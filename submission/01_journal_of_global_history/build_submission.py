#!/usr/bin/env python3
"""
JGH Submission Builder
======================
Reads author_config.ini and generates ALL submission documents:
  - manuscript_jgh.md / .docx  (footnoted, anonymized)
  - title_page.md / .docx
  - cover_letter.md / .docx

Usage:
    python build_submission.py          # builds everything
    python build_submission.py --check  # dry run

No external dependencies — uses only Python stdlib + pandoc for .docx.
"""

import configparser
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent.parent
PAPER_DIR = PROJECT_DIR / "archive" / "paper"
DATA_DIR = PROJECT_DIR / "data"
CONFIG_PATH = SCRIPT_DIR / "author_config.ini"


# ── Bibliography ─────────────────────────────────────────────────────────────
BIBLIOGRAPHY = {
    "Allen 2009": 'Robert C. Allen, _The British Industrial Revolution in Global Perspective_ (Cambridge: Cambridge University Press, 2009).',
    "Angrist and Pischke 2009": "Joshua D. Angrist and Jörn-Steffen Pischke, _Mostly Harmless Econometrics: An Empiricist's Companion_ (Princeton: Princeton University Press, 2009).",
    "Bertrand, Duflo, and Mullainathan 2004": 'Marianne Bertrand, Esther Duflo, and Sendhil Mullainathan, "How Much Should We Trust Differences-in-Differences Estimates?", _Quarterly Journal of Economics_ 119, no. 1 (2004): 249–275.',
    "Bertrand et al. 2004": 'Bertrand, Duflo, and Mullainathan, "How Much Should We Trust Differences-in-Differences Estimates?".',
    "Bertrand et al.": 'Bertrand, Duflo, and Mullainathan, "How Much Should We Trust Differences-in-Differences Estimates?".',
    "Bogart 2024": 'Dan Bogart, _The Transport Revolution in Industrializing Britain: A Survey_ (Cambridge: Cambridge University Press, 2024).',
    "Bolt and van Zanden 2020": 'Jutta Bolt and Jan Luiten van Zanden, "Maddison Style Estimates of the Evolution of the World Economy: A New 2020 Update", _Maddison-Project Working Paper_, WP-154 (2020).',
    "Broadberry et al. 2015": 'Stephen Broadberry et al., _British Economic Growth, 1270–1870_ (Cambridge: Cambridge University Press, 2015).',
    "Cameron, Gelbach, and Miller 2008": 'A. Colin Cameron, Jonah B. Gelbach, and Douglas L. Miller, "Bootstrap-Based Improvements for Inference with Clustered Errors", _Review of Economics and Statistics_ 90, no. 3 (2008): 414–427.',
    "Chernozhukov et al. 2018": 'Victor Chernozhukov et al., "Double/Debiased Machine Learning for Treatment and Structural Parameters", _The Econometrics Journal_ 21, no. 1 (2018): C1–C68.',
    "Crafts 1985": 'Nicholas F. R. Crafts, _British Economic Growth during the Industrial Revolution_ (Oxford: Clarendon Press, 1985).',
    "De Chaisemartin and D'Haultfœuille 2020": "Clément de Chaisemartin and Xavier D'Haultfœuille, \"Two-Way Fixed Effects Estimators with Heterogeneous Treatment Effects\", _American Economic Review_ 110, no. 9 (2020): 2964–2996.",
    "Kanefsky and Robey 1980": 'John Kanefsky and John Robey, "Steam Engines in 18th-Century Britain: A Quantitative Assessment", _Technology and Culture_ 21, no. 2 (1980): 161–186.',
    "Landes 1969": 'David S. Landes, _The Unbound Prometheus: Technological Change and Industrial Development in Western Europe from 1750 to the Present_ (Cambridge: Cambridge University Press, 1969).',
    "Malm 2016": 'Andreas Malm, _Fossil Capital: The Rise of Steam Power and the Roots of Global Warming_ (London: Verso, 2016).',
    "Marx 1847": 'Karl Marx, _The Poverty of Philosophy_ (1847; repr., Moscow: Progress Publishers, 1955).',
    "McCloskey 2010": "Deirdre N. McCloskey, _Bourgeois Dignity: Why Economics Can't Explain the Modern World_ (Chicago: University of Chicago Press, 2010).",
    "Michel et al. 2011": 'Jean-Baptiste Michel et al., "Quantitative Analysis of Culture Using Millions of Digitized Books", _Science_ 331, no. 6014 (2011): 176–82.',
    "Mokyr 2009": 'Joel Mokyr, _The Enlightened Economy: An Economic History of Britain 1700–1850_ (New Haven: Yale University Press, 2009).',
    "Musson and Robinson 1969": 'Albert E. Musson and Eric Robinson, _Science and Technology in the Industrial Revolution_ (Manchester: Manchester University Press, 1969).',
    "Pechenick et al. 2015": 'Eitan Adam Pechenick, Christopher M. Danforth, and Peter Sheridan Dodds, "Characterizing the Google Books Corpus: Strong Limits to Inferences of Socio-Cultural and Linguistic Evolution", _PLOS ONE_ 10, no. 10 (2015): e0137041.',
    "Pomeranz 2000": 'Kenneth Pomeranz, _The Great Divergence: China, Europe, and the Making of the Modern World Economy_ (Princeton: Princeton University Press, 2000).',
    "Rambachan and Roth 2023": 'Ashesh Rambachan and Jonathan Roth, "A More Credible Approach to Parallel Trends", _Review of Economic Studies_ 90, no. 5 (2023): 2555–2591.',
    "Roth et al. 2023": "Jonathan Roth et al., \"What's Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature\", _Journal of Econometrics_ 235, no. 2 (2023): 2218–2244.",
    "Tvedt 2010": 'Terje Tvedt, "Why England and Not China and India? Water Systems and the History of the Industrial Revolution", _Journal of Global History_ 5, no. 1 (2010): 29–50.',
    "Wrigley 2010": 'E. A. Wrigley, _Energy and the English Industrial Revolution_ (Cambridge: Cambridge University Press, 2010).',
}


# ── Config ───────────────────────────────────────────────────────────────────
def load_config() -> dict:
    """Load author_config.ini into a flat dict."""
    if not CONFIG_PATH.exists():
        print(f"ERROR: {CONFIG_PATH} not found.")
        sys.exit(1)

    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH)

    cfg = {
        "author_name": parser.get("author", "name", fallback="[AUTHOR NAME]"),
        "department": parser.get("author", "department", fallback="[Department]"),
        "institution": parser.get("author", "institution", fallback="[Institution]"),
        "city": parser.get("author", "city", fallback="[City]"),
        "country": parser.get("author", "country", fallback="[Country]"),
        "email": parser.get("author", "email", fallback="[email]"),
        "orcid": parser.get("author", "orcid", fallback=""),
        "date": parser.get("submission", "date", fallback="today"),
        "acknowledgments": parser.get("declarations", "acknowledgments", fallback=""),
        "funding": parser.get("declarations", "funding", fallback="This research received no external funding."),
        "competing_interests": parser.get("declarations", "competing_interests", fallback="The author(s) declare no competing interests."),
    }

    if cfg["date"].lower() == "today":
        cfg["date"] = date.today().strftime("%d %B %Y")

    # Warn on unfilled fields
    for field in ["author_name", "department", "institution", "email"]:
        val = cfg[field]
        if val.startswith("Your ") or val.startswith("["):
            print(f"  ⚠️  '{field}' looks unfilled — update author_config.ini")

    return cfg


# ── Manuscript ───────────────────────────────────────────────────────────────
def convert_to_footnotes(text: str) -> str:
    footnotes = []
    counter = [0]
    seen = {}

    def repl(match):
        raw = match.group(1).strip()
        parts = [p.strip() for p in raw.split(';')]
        note_parts = []
        for part in parts:
            ref = BIBLIOGRAPHY.get(part)
            if ref:
                if part in seen:
                    note_parts.append(f'{part}.')
                else:
                    seen[part] = True
                    note_parts.append(ref)
            else:
                note_parts.append(f'{part}.')
        counter[0] += 1
        footnotes.append(f'[^{counter[0]}]: {" ".join(note_parts)}')
        return f'[^{counter[0]}]'

    pattern = r'\((?![\$\\])([A-Z][a-zéœ]+(?: (?:and|et al\.?|,) [A-Za-zéœ\']+)* \d{4}(?:;\s*[A-Z][a-zéœ]+(?: (?:and|et al\.?|,) [A-Za-zéœ\']+)* \d{4})*)\)'
    text = re.sub(pattern, repl, text)
    if footnotes:
        text += '\n\n---\n\n' + '\n'.join(footnotes)
    return text


def fix_for_docx(text: str) -> str:
    """Fix math/dollar issues so Pandoc produces clean Word output.
    
    Two problems:
    1. Currency $ signs (e.g., ~$1,251) confuse Pandoc's LaTeX parser
    2. Double-escaped backslashes from markdown compilation (\\\\alpha → \\alpha)
    """
    # Step 1: Remove currency dollar signs — replace with plain text
    # The context "GDP per capita" already implies the unit
    text = text.replace('~\\\\$1,251', '~1,251')
    text = text.replace('~\\$1,251', '~1,251')
    text = text.replace('~$1,251', '~1,251')
    text = text.replace('\\$1,251', '1,251')
    text = text.replace('additional ~$1,251 in', 'additional ~1,251 in')
    text = text.replace('additional ~\\\\$1,251 in', 'additional ~1,251 in')
    text = text.replace('approximately $1,251', 'approximately 1,251')
    text = text.replace('approximately \\$1,251', 'approximately 1,251')
    
    # Step 2: Fix double-escaped LaTeX backslashes
    # The compiled_manuscript.md has \\\\alpha instead of \\alpha
    text = text.replace('\\\\alpha', '\\alpha')
    text = text.replace('\\\\beta', '\\beta')
    text = text.replace('\\\\gamma', '\\gamma')
    text = text.replace('\\\\delta', '\\delta')
    text = text.replace('\\\\epsilon', '\\epsilon')
    text = text.replace('\\\\text', '\\text')
    text = text.replace('\\\\times', '\\times')
    text = text.replace('\\\\sum', '\\sum')
    text = text.replace('\\\\mathbb', '\\mathbb')
    text = text.replace('\\\\ge', '\\ge')
    
    # Step 3: Fix table dollar signs (e.g., "1990 GK$" in stats tables)
    text = text.replace('GK$)', 'GK\\$)')
    
    # Step 4: Fix LaTeX thousand separator: 1{,}250.9 → 1,250.9
    text = text.replace('{,}', ',')
    
    # Step 5: Normalize display math double-backslashes
    # The compiled manuscript has $$ Y_{it} = \\alpha ... $$ 
    # which needs single backslashes for Pandoc OMML rendering
    import re as _re
    def _fix_display_math(m):
        content = m.group(0)
        content = content.replace('\\\\', '\\')
        return content
    text = _re.sub(r'\$\$.*?\$\$', _fix_display_math, text, flags=_re.DOTALL)
    
    # Step 6: Convert HTML <img> tags to Markdown images with absolute paths
    # The source uses <img src="../../data/file.png"> which Pandoc can't resolve
    # Convert to ![alt](absolute_path) so figures are embedded in the .docx
    def _fix_img_tag(m):
        src = m.group(1)
        alt = m.group(2) if m.group(2) else ''
        # Resolve relative path to absolute
        abs_path = (SCRIPT_DIR / src).resolve()
        if abs_path.exists():
            return f'![{alt}]({abs_path})'
        else:
            return m.group(0)  # leave unchanged if file not found
    text = _re.sub(
        r'<img\s+src="([^"]+)"\s+alt="([^"]*)"\s*(?:width="[^"]*")?\s*/?>',
        _fix_img_tag, text
    )
    
    return text


def build_manuscript() -> Path:
    source = PAPER_DIR / "compiled_manuscript.md"
    if not source.exists():
        print(f"  ERROR: {source} not found. Run compile_paper.py first.")
        sys.exit(1)

    text = source.read_text()
    # Strip references section
    text = re.sub(r'\n# 8\. References.*?(?=\n# |\Z)', '', text, flags=re.DOTALL)
    # Convert citations
    text = convert_to_footnotes(text)
    # Anonymize
    text = text.replace('https://github.com/percw/water_and_society', '[REPOSITORY URL REDACTED FOR REVIEW]')
    text = text.replace('percw/water_and_society', '[REPOSITORY REDACTED]')
    # Fix dollar signs and math for clean docx conversion
    text = fix_for_docx(text)

    header = '---\ntitle: "The Linguistic Hydro-Social Cycle: Water Infrastructure as a Precondition for British Industrialization"\njournal: Journal of Global History\ntype: Original Research Article\nword_count: ~8,000\n---\n\n'

    out = SCRIPT_DIR / "manuscript_jgh.md"
    out.write_text(header + text)
    words = len(text.split())
    fn = text.count('[^') // 2
    print(f"  ✅ Manuscript:    manuscript_jgh.md  ({words} words, {fn} footnotes)")
    return out


# ── Title Page ───────────────────────────────────────────────────────────────
def build_title_page(cfg: dict) -> Path:
    orcid = f"ORCID: {cfg['orcid']}" if cfg['orcid'] else "ORCID: —"
    ack = cfg['acknowledgments'] or "None."

    # Build affiliation line
    affil_parts = [p for p in [cfg['department'], cfg['institution']] if p]
    affil_line = ', '.join(affil_parts)
    loc_parts = [p for p in [cfg['city'], cfg['country']] if p]
    loc_line = ', '.join(loc_parts)

    content = f"""# Title Page

> **CONFIDENTIAL — This page is for editorial use only and must not be sent to reviewers.**

---

## Title

**The Linguistic Hydro-Social Cycle: Water Infrastructure as a Precondition for British Industrialization**

---

## Author(s)

**{cfg['author_name']}**
{affil_line}
{loc_line}
Email: {cfg['email']}
{orcid}

---

## Corresponding Author

{cfg['author_name']} — {cfg['email']}

---

## Keywords

1. Industrial Revolution
2. Water infrastructure
3. Canal engineering
4. Great Divergence
5. Difference-in-differences
6. Natural language processing
7. Geographical symbiosis
8. British economic history
9. Hydro-social
10. Bridgewater Canal

---

## Acknowledgments

{ack}

---

## Funding Statement

{cfg['funding']}

---

## Competing Interests Declaration

{cfg['competing_interests']}

---

## Data Availability Statement

All data and code required to reproduce the analyses in this paper are publicly available at https://github.com/percw/water_and_society. Historical GDP per capita data are sourced from the Maddison Project Database 2023 (Bolt and van Zanden 2020). Linguistic frequency data are drawn from the Google Books Ngram Corpus (`eng_gb_2019`). A self-contained replication package is available as a supplementary archive.

---

## Word Count

Approximately 8,000 words (including footnotes).
"""
    out = SCRIPT_DIR / "title_page.md"
    out.write_text(content)
    print(f"  ✅ Title page:    title_page.md")
    return out


# ── Cover Letter ─────────────────────────────────────────────────────────────
def build_cover_letter(cfg: dict) -> Path:
    """Generate the cover letter from config."""
    affil_parts = [p for p in [cfg['department'], cfg['institution']] if p]
    affil_line = ', '.join(affil_parts)
    content = f"""# Cover Letter — Journal of Global History

---

**{cfg['date']}**

**To:** The Editors, *Journal of Global History*
Cambridge University Press

---

Dear Editors,

I am pleased to submit the manuscript entitled **"The Linguistic Hydro-Social Cycle: Water Infrastructure as a Precondition for British Industrialization"** for consideration as an original research article in the *Journal of Global History*.

This paper builds directly on the theoretical framework established by Terje Tvedt in "Why England and not China and India? Water Systems and the History of the Industrial Revolution," published in this journal in 2010. Where Tvedt proposed that Britain's unique hydro-topographical endowments functioned as a critical precursor to the steam revolution, our study provides the first quantitative test of this hypothesis by merging natural language processing (NLP) of historical print culture with formal Difference-in-Differences (DiD) econometric modeling.

**Key findings:**

- Using a 71-term vocabulary index applied to the Google Books British English corpus (1700–1900), we identify a permanent structural crossover in 1766 at which engineered water terminology overtook naturalistic water terminology in British print culture — five years after the exogenous shock of the Bridgewater Canal opening (1761).
- A DiD framework anchored to the 1761 Canal opening, deployed across an expanded 13-country panel from the Maddison Project Database, estimates that Britain's post-shock trajectory diverged by approximately 1,251 GDP per capita relative to European controls (p = 0.042, HAC-corrected). Magnitude metrics confirm a very large effect (Cohen's d = 1.2–1.5, representing ~50% of pre-treatment British GDP).
- Counterfactual analysis suggests 47% of Britain's ultimate industrial lead was established by 1810 — during the canal and water wheel era, before steam power achieved commercial dominance.
- Placebo falsification tournaments across rival vocabularies (coal, textiles, finance, agriculture) confirm that only the water infrastructure shock uniquely predicts the timing of GDP divergence.

We believe this paper is particularly well-suited to the *Journal of Global History* for three reasons. First, it provides empirical validation of a framework your readership already knows, extending Tvedt's qualitative argument with formal econometric evidence. Second, the comparative dimension — using an expanded panel of 13 countries including France, the Netherlands, Germany, Spain, Japan, China, and India as controls — directly engages the Great Divergence debate central to the journal's intellectual tradition. Third, the paper includes historical illustrations comparing English canal infrastructure with Asian river transport, underscoring the geographical specificity of Britain's water engineering advantage.

The manuscript is approximately 8,000 words including footnotes. A full replication package (data, code, and documentation) is publicly available at https://github.com/percw/water_and_society.

This manuscript has not been submitted to or published in any other journal. {cfg['competing_interests']} {cfg['funding']}

I look forward to your consideration.

Sincerely,

**{cfg['author_name']}**
{affil_line}
{cfg['email']}
"""
    out = SCRIPT_DIR / "cover_letter.md"
    out.write_text(content)
    print(f"  ✅ Cover letter:  cover_letter.md")
    return out


# ── DOCX ─────────────────────────────────────────────────────────────────────
def to_docx(md_path: Path) -> Path:
    docx = md_path.with_suffix('.docx')
    try:
        subprocess.run(['pandoc', str(md_path), '-o', str(docx), '--standalone'],
                       check=True, capture_output=True)
        kb = docx.stat().st_size // 1024
        print(f"  ✅ Word export:   {docx.name}  ({kb} KB)")
        return docx
    except FileNotFoundError:
        print(f"  ⚠️  pandoc not found — skipping .docx for {md_path.name}")
        return None
    except subprocess.CalledProcessError as e:
        print(f"  ❌ pandoc error: {e.stderr.decode()}")
        return None


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    check = "--check" in sys.argv

    print()
    print("=" * 60)
    print("  JGH Submission Builder")
    print("=" * 60)
    print()

    cfg = load_config()
    print(f"  Author:  {cfg['author_name']}")
    print(f"  Affil:   {cfg['department']}, {cfg['institution']}")
    print(f"  Email:   {cfg['email']}")
    print(f"  Date:    {cfg['date']}")
    print()

    if check:
        print("  [DRY RUN — no files written]")
        print()
        return

    print("  Building documents...")
    print("  " + "-" * 40)
    ms = build_manuscript()
    tp = build_title_page(cfg)
    cl = build_cover_letter(cfg)

    print()
    print("  Converting to Word (.docx)...")
    print("  " + "-" * 40)
    to_docx(ms)
    to_docx(tp)
    to_docx(cl)

    print()
    print("=" * 60)
    print("  ✅ ALL DONE — Submission package ready!")
    print("=" * 60)
    print()
    print("  Upload to Cambridge portal:")
    print("    1. manuscript_jgh.docx")
    print("    2. title_page.docx        (editors only)")
    print("    3. cover_letter.docx")
    print("    4. data/did_figure_one.png")
    print("    5. data/did_event_study.png")
    print("    6. data/did_vocab_tournament.png")
    print()


if __name__ == '__main__':
    main()
