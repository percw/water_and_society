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
    'Allen 2009': 'Robert C. Allen, _The British Industrial Revolution in Global Perspective_ (Cambridge: Cambridge University Press, 2009).',
    'Alvarez-Palau et al. 2024': 'Eduard J. Alvarez-Palau, Dan Bogart, Max Satchell, and Leigh Shaw-Taylor, “Transport and Urban Growth in the First Industrial Revolution”, _Economic Journal_ 135, no. 668 (2024): 1191–1228.',
    'Andrews 1993': 'Donald W. K. Andrews, “Tests for Parameter Instability and Structural Change with Unknown Change Point”, _Econometrica_ 61, no. 4 (1993): 821–856.',
    'Bai and Perron 1998': 'Jushan Bai and Pierre Perron, “Estimating and Testing Linear Models with Multiple Structural Changes”, _Econometrica_ 66, no. 1 (1998): 47–78.',
    'Bertrand, Duflo, and Mullainathan 2004': 'Marianne Bertrand, Esther Duflo, and Sendhil Mullainathan, “How Much Should We Trust Differences-in-Differences Estimates?”, _Quarterly Journal of Economics_ 119, no. 1 (2004): 249–275.',
    'Bogart 2014': 'Dan Bogart, “The Transport Revolution in Industrialising Britain: A Survey”, in _The Cambridge Economic History of Modern Britain, Volume 1: 1700–1870_, ed. Roderick Floud, Jane Humphries, and Paul Johnson (Cambridge: Cambridge University Press, 2014), 368–391.',
    'Bolt and van Zanden 2024': 'Jutta Bolt and Jan Luiten van Zanden, “Maddison-Style Estimates of the Evolution of the World Economy: A New 2023 Update”, _Journal of Economic Surveys_ 39, no. 2 (2024): 631–671.',
    'Broadberry et al. 2015': 'Stephen Broadberry, Bruce M. S. Campbell, Alexander Klein, Mark Overton, and Bas van Leeuwen, _British Economic Growth, 1270–1870_ (Cambridge: Cambridge University Press, 2015).',
    'Clark and Jacks 2007': 'Gregory Clark and David Jacks, “Coal and the Industrial Revolution, 1700–1869”, _European Review of Economic History_ 11, no. 1 (2007): 39–72.',
    'Crafts 1985': 'Nicholas F. R. Crafts, _British Economic Growth during the Industrial Revolution_ (Oxford: Clarendon Press, 1985).',
    'Crafts 2004': 'Nicholas F. R. Crafts, “Steam as a General Purpose Technology: A Growth Accounting Perspective”, _Economic Journal_ 114, no. 495 (2004): 338–351.',
    'Crafts and Harley 1992': 'Nicholas F. R. Crafts and C. Knick Harley, “Output Growth and the British Industrial Revolution: A Restatement of the Crafts–Harley View”, _Economic History Review_ 45, no. 4 (1992): 703–730.',
    'Crouzet 1964': 'François Crouzet, “Wars, Blockade, and Economic Change in Europe, 1792–1815”, _Journal of Economic History_ 24, no. 4 (1964): 567–588.',
    'de Vries 1978': 'Jan de Vries, _Barges and Capitalism: Passenger Transportation in the Dutch Economy, 1632–1839_ (Utrecht: HES Publishers, 1978).',
    "Fernihough and O'Rourke 2021": "Alan Fernihough and Kevin Hjortshøj O'Rourke, “Coal and the European Industrial Revolution”, _Economic Journal_ 131, no. 635 (2021): 1135–1149.",
    'Hadfield 1984': 'Charles Hadfield, _British Canals: An Illustrated History_, 7th ed. (Newton Abbot: David and Charles, 1984).',
    'Jordà 2005': 'Òscar Jordà, “Estimation and Inference of Impulse Responses by Local Projections”, _American Economic Review_ 95, no. 1 (2005): 161–182.',
    'Kanefsky 1979': 'John W. Kanefsky, “The Diffusion of Power Technology in British Industry, 1760–1870” (PhD thesis, University of Exeter, 1979).',
    'Kanefsky and Robey 1980': 'John Kanefsky and John Robey, “Steam Engines in 18th-Century Britain: A Quantitative Assessment”, _Technology and Culture_ 21, no. 2 (1980): 161–186.',
    'Landes 1969': 'David S. Landes, _The Unbound Prometheus_ (Cambridge: Cambridge University Press, 1969).',
    'Malm 2016': 'Andreas Malm, _Fossil Capital: The Rise of Steam Power and the Roots of Global Warming_ (London: Verso, 2016).',
    'Michel et al. 2011': 'Jean-Baptiste Michel et al., “Quantitative Analysis of Culture Using Millions of Digitized Books”, _Science_ 331, no. 6014 (2011): 176–182.',
    'Newey and West 1987': 'Whitney K. Newey and Kenneth D. West, “A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix”, _Econometrica_ 55, no. 3 (1987): 703–708.',
    'Pechenick et al. 2015': 'Eitan Adam Pechenick, Christopher M. Danforth, and Peter Sheridan Dodds, “Characterizing the Google Books Corpus: Strong Limits to Inferences of Socio-Cultural and Linguistic Evolution”, _PLOS ONE_ 10, no. 10 (2015): e0137041.',
    'Pomeranz 2000': 'Kenneth Pomeranz, _The Great Divergence: China, Europe, and the Making of the Modern World Economy_ (Princeton: Princeton University Press, 2000).',
    'Priestley 1831': 'Joseph Priestley, _Historical Account of the Navigable Rivers, Canals, and Railways, throughout Great Britain_ (London: Longman, Rees, Orme, Brown and Green, 1831).',
    'Rambachan and Roth 2023': 'Ashesh Rambachan and Jonathan Roth, “A More Credible Approach to Parallel Trends”, _Review of Economic Studies_ 90, no. 5 (2023): 2555–2591.',
    'Roth et al. 2023': "Jonathan Roth, Pedro H. C. Sant'Anna, Alyssa Bilinski, and John Poe, “What's Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature”, _Journal of Econometrics_ 235, no. 2 (2023): 2218–2244.",
    'Szostak 1991': "Rick Szostak, _The Role of Transportation in the Industrial Revolution: A Comparison of England and France_ (Montreal: McGill-Queen's University Press, 1991).",
    'Thomas and Dimsdale 2017': 'Ryland Thomas and Nicholas Dimsdale, _A Millennium of UK Data_, Bank of England OBRA dataset (2017).',
    'Turnbull 1987': 'Gerard Turnbull, “Canals, Coal and Regional Growth during the Industrial Revolution”, _Economic History Review_ 40, no. 4 (1987): 537–560.',
    'Tvedt 2010': 'Terje Tvedt, “Why England and Not China and India? Water Systems and the History of the Industrial Revolution”, _Journal of Global History_ 5, no. 1 (2010): 29–50.',
    'Ward 1974': 'J. R. Ward, _The Finance of Canal Building in Eighteenth-Century England_ (Oxford: Oxford University Press, 1974).',
    'Wrigley 1988': 'E. A. Wrigley, _Continuity, Chance and Change: The Character of the Industrial Revolution in England_ (Cambridge: Cambridge University Press, 1988).',
    'Wrigley 2010': 'E. A. Wrigley, _Energy and the English Industrial Revolution_ (Cambridge: Cambridge University Press, 2010).',
    'Wrigley 2016': "E. A. Wrigley, _The Path to Sustained Growth: England's Transition from an Organic Economy to an Industrial Revolution_ (Cambridge: Cambridge University Press, 2016).",
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
        "biography": parser.get("author", "biography", fallback="[AUTHOR BIOGRAPHY, max 100 words]"),
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
        if not any(p in BIBLIOGRAPHY for p in parts):
            return match.group(0)
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

    pattern = r"\((?![\$\\])((?:[A-Za-z][\w'’\-\.]*[ ,]*)+? \d{4}[a-z]?(?:;\s*(?:[A-Za-z][\w'’\-\.]*[ ,]*)+? \d{4}[a-z]?)*)\)"
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
            return f'![{alt}]({src})'
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

    header = '---\ntitle: "Water Before Steam: Canals, Coal and the Making of Britain\'s Fossil Economy, 1700–1870"\njournal: Journal of Global History\ntype: Original Research Article\nword_count: ~9,300\n---\n\n'

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

**Water Before Steam: Canals, Coal and the Making of Britain's Fossil Economy, 1700–1870**

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
2. Canals
3. Coal
4. Water infrastructure
5. Growth regimes
6. Great Divergence
7. Google Books Ngram
8. British economic history
9. Steam power
10. Transport revolution

---

## Author Biography

{cfg['biography']}

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

All code and data required to reproduce the analyses are publicly available at https://github.com/percw/water_and_society. British sectoral output and population are from the Bank of England's *A Millennium of Macroeconomic Data for the UK*, reproducing Broadberry et al. (2015). Cross-country GDP per head and population are from the Maddison Project Database 2023 (Bolt and van Zanden 2024). Installed horsepower is from Kanefsky (1979) via Crafts (2004). Canal completion years and parliamentary authorisations (Priestley 1831) are included with their construction scripts. Word and phrase frequencies are from the Google Books Ngram Corpus, British English 2019 edition. A self-contained replication package is available as a supplementary archive.

---

## Word Count

Approximately 9,300 words (including footnotes and tables).
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

I am pleased to submit the manuscript **"Water Before Steam: Canals, Coal and the Making of Britain's Fossil Economy, 1700–1870"** for consideration as an original research article in the *Journal of Global History*.

The paper is a quantitative test of the argument Terje Tvedt made in this journal in 2010: that Britain's water systems were the precondition for its coal-based industrialisation rather than a rival to it. Using annual British sectoral output for 1700–1870, a new year-by-year series of canal mileage, installed steam and water horsepower, the Maddison Project Database 2023 and the Google Books British corpus, we show that Britain passed through two growth regimes. Aggregate output, coal, iron and population accelerated between 1775 and 1792 as the canal network was built, while income per head did not move; income per head accelerated only after 1818, once steam was becoming the majority power source. Canal mileage predicts coal output over the following two decades and predicts population, but not income per head or agriculture. Steam raises income per head only after 1830. In print, “coal barge” and “coal wharf” precede “steam engine” and “steam power” by a generation.

**Why this journal.** The paper engages Tvedt (2010) directly and extends the Great Divergence debate with the comparative case his argument needs: the Netherlands, with Europe's densest waterways and no coal, grew 9 per cent in total output between 1700 and 1820; Britain, with both, grew 240 per cent. The paper also contains a methodological result for historians who use cross-country difference-in-differences for the long eighteenth century: the apparent British take-off in 1807 in such designs is the Napoleonic collapse of the continental control group. We withdraw an earlier version's estimate on exactly that ground and explain why.

The manuscript is approximately 9,300 words including footnotes and tables, with six figures and seven tables. A full replication package (data, code and documentation) is publicly available at https://github.com/percw/water_and_society.

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


def double_space_docx(docx: Path) -> None:
    """JGH asks for double-spaced text. Set line spacing to 480 (= 2.0) in the document defaults
    and in the body/first-paragraph styles, leaving tables, footnotes and captions untouched."""
    import zipfile, shutil, re as _re
    tmp = docx.with_suffix('.tmp.docx')
    with zipfile.ZipFile(docx) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == 'word/styles.xml':
                xml = data.decode('utf8')
                # document defaults
                if '<w:pPrDefault>' in xml:
                    xml = _re.sub(r'<w:pPrDefault>\s*<w:pPr>', '<w:pPrDefault><w:pPr><w:spacing w:line="480" w:lineRule="auto"/>', xml, count=1)
                    xml = xml.replace('<w:pPrDefault/>', '<w:pPrDefault><w:pPr><w:spacing w:line="480" w:lineRule="auto"/></w:pPr></w:pPrDefault>')
                else:
                    xml = xml.replace('<w:docDefaults>', '<w:docDefaults><w:pPrDefault><w:pPr><w:spacing w:line="480" w:lineRule="auto"/></w:pPr></w:pPrDefault>', 1)
                # pandoc body styles carry their own spacing; override line spacing there too
                for sid in ('BodyText', 'FirstParagraph'):
                    xml = _re.sub(r'(<w:style [^>]*w:styleId="%s"[^>]*>.*?<w:pPr>)(.*?)(</w:pPr>)' % sid,
                                  lambda m: m.group(1) + _re.sub(r'<w:spacing[^>]*/>', '', m.group(2)) + '<w:spacing w:before="0" w:after="180" w:line="480" w:lineRule="auto"/>' + m.group(3),
                                  xml, count=1, flags=_re.DOTALL)
                # footnotes and tables stay single-spaced
                for sid in ('FootnoteText', 'Compact', 'TableCaption', 'ImageCaption', 'Caption'):
                    xml = _re.sub(r'(<w:style [^>]*w:styleId="%s"[^>]*>.*?<w:pPr>)(.*?)(</w:pPr>)' % sid,
                                  lambda m: m.group(1) + _re.sub(r'<w:spacing[^>]*/>', '', m.group(2)) + '<w:spacing w:line="240" w:lineRule="auto"/>' + m.group(3),
                                  xml, count=1, flags=_re.DOTALL)
                data = xml.encode('utf8')
            zout.writestr(item, data)
    shutil.move(tmp, docx)


# ── DOCX ─────────────────────────────────────────────────────────────────────
def to_docx(md_path: Path) -> Path:
    docx = md_path.with_suffix('.docx')
    try:
        subprocess.run(['pandoc', str(md_path), '-o', str(docx), '--standalone'], cwd=str(SCRIPT_DIR),
                       check=True, capture_output=True)
        if md_path.name.startswith('manuscript'):
            double_space_docx(docx)
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
    print("    4. data/fig1_two_regimes.png … data/fig6_power_benchmark.png (six figures)")
    print()


if __name__ == '__main__':
    main()
