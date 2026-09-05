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
    'Alvarez-Palau et al. 2025': 'Eduard J. Alvarez-Palau, Dan Bogart, Max Satchell, and Leigh Shaw-Taylor, “Transport and Urban Growth in the First Industrial Revolution”, _Economic Journal_ 135, no. 668 (2025): 1191–1228.',
    'Andrews 1993': 'Donald W. K. Andrews, “Tests for Parameter Instability and Structural Change with Unknown Change Point”, _Econometrica_ 61, no. 4 (1993): 821–856.',
    'Bai and Perron 1998': 'Jushan Bai and Pierre Perron, “Estimating and Testing Linear Models with Multiple Structural Changes”, _Econometrica_ 66, no. 1 (1998): 47–78.',
    'Bertrand, Duflo, and Mullainathan 2004': 'Marianne Bertrand, Esther Duflo, and Sendhil Mullainathan, “How Much Should We Trust Differences-in-Differences Estimates?”, _Quarterly Journal of Economics_ 119, no. 1 (2004): 249–275.',
    'Bogart 2014': 'Dan Bogart, “The Transport Revolution in Industrialising Britain: A Survey”, in _The Cambridge Economic History of Modern Britain, Volume 1: 1700–1870_, ed. Roderick Floud, Jane Humphries, and Paul Johnson (Cambridge: Cambridge University Press, 2014), 368–391.',
    'Bolt and van Zanden 2025': 'Jutta Bolt and Jan Luiten van Zanden, “Maddison-Style Estimates of the Evolution of the World Economy: A New 2023 Update”, _Journal of Economic Surveys_ 39, no. 2 (2025): 631–671.',
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
    'Priestley 1831': 'Joseph Priestley, _Historical Account of the Navigable Rivers, Canals, and Railways, throughout Great Britain_ (Longman, Rees, Orme, Brown and Green, 1831).',
    'Rambachan and Roth 2023': 'Ashesh Rambachan and Jonathan Roth, “A More Credible Approach to Parallel Trends”, _Review of Economic Studies_ 90, no. 5 (2023): 2555–2591.',
    'Roth et al. 2023': "Jonathan Roth, Pedro H. C. Sant'Anna, Alyssa Bilinski, and John Poe, “What's Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature”, _Journal of Econometrics_ 235, no. 2 (2023): 2218–2244.",
    'Szostak 1991': "Rick Szostak, _The Role of Transportation in the Industrial Revolution: A Comparison of England and France_ (Montreal: McGill-Queen's University Press, 1991).",
    'Thomas and Dimsdale 2017': 'Ryland Thomas and Nicholas Dimsdale, _A Millennium of UK Data_, Bank of England OBRA dataset (2017).',
    'Turnbull 1987': 'Gerard Turnbull, “Canals, Coal and Regional Growth during the Industrial Revolution”, _Economic History Review_ 40, no. 4 (1987): 537–560.',
    'Tvedt 2010': 'Terje Tvedt, “Why England and Not China and India? Water Systems and the History of the Industrial Revolution”, _Journal of Global History_ 5, no. 1 (2010): 29–50.',
    'Ward 1974': 'J. R. Ward, _The Finance of Canal Building in Eighteenth-Century England_ (Oxford: Oxford University Press, 1974).',
    'Wrigley 1988': 'E. A. Wrigley, _Continuity, Chance and Change: The Character of the Industrial Revolution in England_ (Cambridge: Cambridge University Press, 1988).',
    'Wrigley 2010': 'E. A. Wrigley, _Energy and the English Industrial Revolution_ (Cambridge: Cambridge University Press, 2010).',
    'Broadberry, Guan, and Li 2018': 'Stephen Broadberry, Hanhui Guan, and David Daokui Li, “China, Europe, and the Great Divergence: A Study in Historical National Accounting, 980–1850”, _Journal of Economic History_ 78, no. 4 (2018): 955–1000.',
    'de Vries and van der Woude 1997': 'Jan de Vries and Ad van der Woude, _The First Modern Economy: Success, Failure, and Perseverance of the Dutch Economy, 1500–1815_ (Cambridge: Cambridge University Press, 1997).',
    'de Zeeuw 1978': 'J. W. de Zeeuw, “Peat and the Dutch Golden Age: The Historical Meaning of Energy-Attainability”, _A.A.G. Bijdragen_ 21 (1978): 3–31.',
    'Flinn 1984': 'Michael W. Flinn, _The History of the British Coal Industry, Volume 2: 1700–1830, The Industrial Revolution_ (Oxford: Clarendon Press, 1984).',
    'Hatcher 1993': 'John Hatcher, _The History of the British Coal Industry, Volume 1: Before 1700_ (Oxford: Clarendon Press, 1993).',
    'Kander, Malanima, and Warde 2013': 'Astrid Kander, Paolo Malanima, and Paul Warde, _Power to the People: Energy in Europe over the Last Five Centuries_ (Princeton: Princeton University Press, 2013).',
    'Maw 2013': 'Peter Maw, _Transport and the Industrial City: Manchester and the Canal Age, 1750–1850_ (Manchester: Manchester University Press, 2013).',
    'Mokyr 1976': 'Joel Mokyr, _Industrialization in the Low Countries, 1795–1850_ (New Haven: Yale University Press, 1976).',
    'Pollard 1980': 'Sidney Pollard, “A New Estimate of British Coal Production, 1750–1850”, _Economic History Review_ 33, no. 2 (1980): 212–235.',
    'Warde 2007': 'Paul Warde, _Energy Consumption in England and Wales, 1560–2000_ (Naples: CNR-ISSM, 2007).',
    'Wrigley 2016': "E. A. Wrigley, _The Path to Sustained Growth: England's Transition from an Organic Economy to an Industrial Revolution_ (Cambridge: Cambridge University Press, 2016).",
}


SHORT_TITLES = {
    'Allen 2009': 'Allen, _British Industrial Revolution_',
    'Alvarez-Palau et al. 2025': 'Alvarez-Palau et al., “Transport and Urban Growth”',
    'Andrews 1993': 'Andrews, “Tests for Parameter Instability”',
    'Bai and Perron 1998': 'Bai and Perron, “Estimating and Testing”',
    'Bertrand, Duflo, and Mullainathan 2004': 'Bertrand, Duflo, and Mullainathan, “How Much Should We Trust”',
    'Bogart 2014': 'Bogart, “Transport Revolution”',
    'Bolt and van Zanden 2025': 'Bolt and van Zanden, “Maddison-Style Estimates”',
    'Broadberry et al. 2015': 'Broadberry et al., _British Economic Growth_',
    'Broadberry, Guan, and Li 2018': 'Broadberry, Guan, and Li, “China, Europe, and the Great Divergence”',
    'Clark and Jacks 2007': 'Clark and Jacks, “Coal and the Industrial Revolution”',
    'Crafts 1985': 'Crafts, _British Economic Growth_',
    'Crafts 2004': 'Crafts, “Steam as a General Purpose Technology”',
    'Crafts and Harley 1992': 'Crafts and Harley, “Output Growth”',
    'Crouzet 1964': 'Crouzet, “Wars, Blockade, and Economic Change”',
    'de Vries 1978': 'de Vries, _Barges and Capitalism_',
    'de Vries and van der Woude 1997': 'de Vries and van der Woude, _First Modern Economy_',
    'de Zeeuw 1978': 'de Zeeuw, “Peat and the Dutch Golden Age”',
    "Fernihough and O'Rourke 2021": "Fernihough and O'Rourke, “Coal and the European Industrial Revolution”",
    'Flinn 1984': 'Flinn, _British Coal Industry_, vol. 2',
    'Hadfield 1984': 'Hadfield, _British Canals_',
    'Hatcher 1993': 'Hatcher, _British Coal Industry_, vol. 1',
    'Jordà 2005': 'Jordà, “Local Projections”',
    'Kander, Malanima, and Warde 2013': 'Kander, Malanima, and Warde, _Power to the People_',
    'Kanefsky 1979': 'Kanefsky, “Diffusion of Power Technology”',
    'Kanefsky and Robey 1980': 'Kanefsky and Robey, “Steam Engines”',
    'Landes 1969': 'Landes, _Unbound Prometheus_',
    'Malm 2016': 'Malm, _Fossil Capital_',
    'Maw 2013': 'Maw, _Transport and the Industrial City_',
    'Michel et al. 2011': 'Michel et al., “Quantitative Analysis of Culture”',
    'Mokyr 1976': 'Mokyr, _Industrialization in the Low Countries_',
    'Newey and West 1987': 'Newey and West, “Simple, Positive Semi-Definite”',
    'Pechenick et al. 2015': 'Pechenick, Danforth, and Dodds, “Characterizing the Google Books Corpus”',
    'Pollard 1980': 'Pollard, “New Estimate”',
    'Pomeranz 2000': 'Pomeranz, _Great Divergence_',
    'Priestley 1831': 'Priestley, _Historical Account_',
    'Rambachan and Roth 2023': 'Rambachan and Roth, “More Credible Approach”',
    'Roth et al. 2023': 'Roth et al., “What’s Trending”',
    'Szostak 1991': 'Szostak, _Role of Transportation_',
    'Thomas and Dimsdale 2017': 'Thomas and Dimsdale, _Millennium of UK Data_',
    'Turnbull 1987': 'Turnbull, “Canals, Coal and Regional Growth”',
    'Tvedt 2010': 'Tvedt, “Why England”',
    'Ward 1974': 'Ward, _Finance of Canal Building_',
    'Warde 2007': 'Warde, _Energy Consumption_',
    'Wrigley 1988': 'Wrigley, _Continuity, Chance and Change_',
    'Wrigley 2010': 'Wrigley, _Energy and the English Industrial Revolution_',
    'Wrigley 2016': 'Wrigley, _Path to Sustained Growth_',
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
        "postal_address": parser.get("author", "postal_address", fallback="[POSTAL ADDRESS]"),
        "ai_declaration": parser.get("declarations", "ai_declaration", fallback=""),
        "date": parser.get("submission", "date", fallback="today"),
        "acknowledgments": parser.get("declarations", "acknowledgments", fallback=""),
        "funding": parser.get("declarations", "funding", fallback="This research received no external funding."),
        "competing_interests": parser.get("declarations", "competing_interests", fallback="The author declares no competing interests."),
    }

    if cfg["date"].lower() == "today":
        cfg["date"] = date.today().strftime("%-d %B %Y")

    # Warn on unfilled fields
    for field in ["author_name", "department", "institution", "email"]:
        val = cfg[field]
        if val.startswith("Your ") or val.startswith("["):
            print(f"  ⚠️  '{field}' looks unfilled — update author_config.ini")

    return cfg


# ── JGH house-style transforms ───────────────────────────────────────────────
def _elide_pages(m):
    a, b = m.group(1), m.group(2)
    if len(a) != len(b) or len(a) < 3:
        return m.group(0)
    # Chicago/JGH: 241–5, 112–13, 1191–228, 2218–44
    i = 0
    while i < len(a) - 1 and a[i] == b[i]:
        i += 1
    if a[-2] == '1' and len(a) - i > 2:  # keep two digits for 10–19 within a hundred
        i = len(a) - 2
    short = b[i:]
    if len(short) == 1 and a[-2] == '1':
        short = b[-2:]
    return f'{a}–{short}'


def chicago18(ref: str) -> str:
    """Chicago 18 / JGH: no place of publication, single curly quotes, elided page ranges, 'PhD diss.'"""
    ref = re.sub(r'\(([A-Z][A-Za-z .\-]+?): ((?:[A-Z][^,()]*?)(?:Press|Publishers|Verso|CNR-ISSM|Charles|Green|Yale University Press)[^,()]*?), (\d{4})\)', r'(\2, \3)', ref)
    ref = re.sub(r'\(([A-Z][A-Za-z .\-]+?): ([^,()]+?), (\d{4})\)', r'(\2, \3)', ref)
    ref = ref.replace('“', '‘').replace('”', '’')
    ref = ref.replace('PhD thesis', 'PhD diss.')
    ref = re.sub(r'(\d{2,4})–(\d{2,4})(?=[.,;)]|$)', _elide_pages, ref)
    return ref


def house_style(text: str) -> str:
    """Body-text conventions: X% not X per cent; 1760–80 within a century; single curly quotes."""
    text = re.sub(r'(\d[\d,.]*)\s+per cent', r'\1%', text)
    text = text.replace('the 7 per cent level', 'the 7% level').replace('at 5 per cent', 'at 5%')
    text = re.sub(r'\b(1[6-9])(\d\d)–\1(\d\d)\b', r'\1\2–\3', text)
    out = []
    for line in text.split('\n'):
        if line.startswith('[^') or line.startswith('<') or line.startswith('!['):
            out.append(line); continue
        line = line.replace('“', '‘').replace('”', '’')
        # straight double quotes -> alternating single curly quotes
        parts = line.split('"')
        if len(parts) > 1:
            line = ''.join(part + (('‘' if i % 2 == 0 else '’') if i < len(parts) - 1 else '') for i, part in enumerate(parts))
        out.append(line)
    return '\n'.join(out)


def footnotes_to_sentence_end(text: str) -> str:
    """Move [^n] markers to the end of their sentence; merge markers that land together; renumber."""
    body, sep, defs = text.partition('\n\n---\n\n[^')
    if not sep:
        return text
    defs = '[^' + defs
    fn = dict(re.findall(r'^\[\^(\d+)\]: (.*)$', defs, flags=re.M))
    marker = re.compile(r'\[\^(\d+)\]')
    sent_end = re.compile(r'[.!?](?=[’”)\]]*(?:\s+[A-Z‘“(\[]|\s*$))')
    protect = [('et al.', 'et al⁠'), ('no.', 'no⁠'), ('vol.', 'vol⁠'), ('p.', 'p⁠'), ('pp.', 'pp⁠'), ('c.', 'c⁠'), ('e.g.', 'e⁠g⁠'), ('i.e.', 'i⁠e⁠')]
    paras = body.split('\n\n')
    new_paras = []
    for para in paras:
        if para.startswith(('#', '|', '<', '![', '*', '**Table', '[Table', '[Figure', '---')) or not marker.search(para):
            new_paras.append(para); continue
        for a, b in protect: para = para.replace(a, b)
        # strip markers, remember their positions
        pos = []; clean = ''; last = 0
        for m in marker.finditer(para):
            clean += para[last:m.start()]; pos.append((len(clean), m.group(1))); last = m.end()
        clean += para[last:]
        ends = [m.end() for m in sent_end.finditer(clean)]
        groups = {}
        for p_, n in pos:
            # marker already just after sentence end?
            target = next((e for e in ends if e >= p_ - 1), len(clean))
            groups.setdefault(target, []).append(n)
        rebuilt = ''; last = 0
        for target in sorted(groups):
            rebuilt += clean[last:target] + ''.join(f'[^{n}]' for n in groups[target]); last = target
        rebuilt += clean[last:]
        for a, b in protect: rebuilt = rebuilt.replace(b, a)
        new_paras.append(rebuilt)
    body = '\n\n'.join(new_paras)
    # merge adjacent markers and renumber sequentially
    counter = [0]; newdefs = []
    def merge(m):
        nums = re.findall(r'\d+', m.group(0)); counter[0] += 1
        texts = [fn.get(n, '').rstrip('.') for n in nums]
        newdefs.append(f'[^{counter[0]}]: ' + '; '.join(t for t in texts if t) + '.')
        return f'[^{counter[0]}]'
    body = re.sub(r'(?:\[\^\d+\])+', merge, body)
    return body + '\n\n---\n\n' + '\n'.join(newdefs)


def tables_to_end(text: str) -> str:
    """Move markdown tables (bold heading, table, italic note) to a Tables section with placeholders."""
    pat = re.compile(r'(\*\*Table (\d+):[^\n]*\*\*\n\n(?:\|[^\n]*\n)+(?:\n\*[^\n]*\*\n)?)')
    tables = []
    def repl(m):
        tables.append(m.group(1).rstrip('\n')); return f'[Table {m.group(2)} about here]\n'
    text = pat.sub(repl, text)
    if tables:
        text += '\n\n# Tables\n\n' + '\n\n'.join(tables) + '\n'
    return text


def figures_to_end(text: str) -> str:
    """Replace inline figure blocks with placeholders + captions; collect figures at the end."""
    pat = re.compile(r'<div align="center">\s*<img src="([^"]+)" alt="Figure (\d+)[^"]*"[^>]*>\s*<br>\s*<em>(.*?)</em>\s*</div>', flags=re.S)
    figs = []
    def repl(m):
        src, n, cap = m.group(1), m.group(2), m.group(3).strip()
        figs.append(f'<img src="{src}" alt="Figure {n}" width="800">\n\n*{cap}*')
        return f'[Figure {n} about here]\n\n*{cap}*'
    text = pat.sub(repl, text)
    if figs:
        text += '\n\n# Figures\n\n' + '\n\n'.join(figs) + '\n'
    return text


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
                ref = chicago18(ref)
                if part in seen:
                    note_parts.append(SHORT_TITLES.get(part, part) + '.')
                else:
                    seen[part] = True
                    note_parts.append(ref)
            else:
                note_parts.append(f'{part}.')
        counter[0] += 1
        footnotes.append(f'[^{counter[0]}]: ' + '; '.join(np.rstrip('.') for np in note_parts) + '.')
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
    text = re.sub(r'\n\n---\n\n', '\n\n', text)
    # Strip references section
    text = re.sub(r'\n# 8\. References.*?(?=\n# |\Z)', '', text, flags=re.DOTALL)
    # JGH house style: unnumbered headings
    text = re.sub(r'^(#{1,3}) \d+(?:\.\d+)*\.? +', r'\1 ', text, flags=re.M)
    # Tables and figures to the end with placeholders (JGH)
    text = tables_to_end(text)
    text = figures_to_end(text)
    # Convert citations, then move markers to sentence ends and merge
    text = convert_to_footnotes(text)
    text = footnotes_to_sentence_end(text)
    # House style: %, year spans, single curly quotes
    text = house_style(text)
    # Anonymize
    text = text.replace('https://github.com/percw/water_and_society', '[REPOSITORY URL REDACTED FOR REVIEW]')
    text = text.replace('percw/water_and_society', '[REPOSITORY REDACTED]')
    # Fix dollar signs and math for clean docx conversion
    text = fix_for_docx(text)

    header = '---\ntitle: "Water Before Steam: Canals, Coal and the Making of Britain\'s Fossil Economy, 1700–1870"\njournal: Journal of Global History\ntype: Original Research Article\nword_count: see title page\n---\n\n'

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
Postal address: {cfg['postal_address']}
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
5. Transport revolution
6. Organic economy
7. Growth regimes
8. Great Divergence

---

## Author Biography

{cfg['biography']}

---

## Acknowledgements

{ack}

{cfg['ai_declaration']}

---

## Financial Support

{cfg['funding']}

---

## Competing Interests Declaration

{cfg['competing_interests']}

---

## Data Availability Statement

All code and data required to reproduce the analyses are publicly available at https://github.com/percw/water_and_society. British sectoral output and population are from the Bank of England's *A Millennium of Macroeconomic Data for the UK*, reproducing Broadberry et al. (2015). Cross-country GDP per head and population are from the Maddison Project Database 2023 (Bolt and van Zanden 2024). Installed horsepower is from Kanefsky (1979) via Crafts (2004). Canal completion years and parliamentary authorisations (Priestley 1831) are included with their construction scripts. Word and phrase frequencies are from the Google Books Ngram Corpus, British English 2019 edition. A self-contained replication package is available as a supplementary archive.

---

## Word Count

Approximately 12,000 words including footnotes, tables and captions (JGH limit 12,500).
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

The paper tests, on annual British data for 1700–1870, the argument Terje Tvedt made in this journal in 2010: that Britain's water systems were the precondition for its coal-based industrialisation rather than a rival to it. It finds two growth regimes, an aggregate acceleration in 1775–1792 that coincided with the building of the canal network and was absorbed by population, and a per-capita acceleration from 1818 that belongs to steam; it shows that canal mileage predicts coal output but not income per head; and it shows, in the language of the Google Books British corpus, that coal travelled by barge a generation before it burned in engines.

**Why this journal.** The paper engages Tvedt directly, adds the comparative benchmarks his argument invites (the Netherlands, Belgium and China) with an explicit account of what a British time series can and cannot say about them, and contains a methodological result for historians who use cross-country difference-in-differences across the Revolutionary and Napoleonic wars: the apparent British take-off of 1807 in such designs is the collapse of the continental control group.

**Use of AI tools.** {cfg['ai_declaration'].replace('Use of AI tools: the author', 'The author', 1)}

**Disclosure for double-anonymous review.** An earlier and substantially different version of this analysis, which reported the cross-country difference-in-differences that the present paper withdraws, has been public in a code repository since spring 2026. The manuscript has been anonymised, but referees who search for the topic may encounter that repository. All figures are the author's own, generated from public data.

The manuscript is approximately 12,000 words including footnotes, tables and captions, with five figures and seven tables. A full replication package (data, code and documentation) is available and the repository URL is given on the title page.

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
    """JGH: one font, double-spaced body. Sets Times New Roman 12pt everywhere, line spacing 2.0 in the
    document defaults and body styles, and single spacing for footnotes, tables and captions."""
    import zipfile, shutil, re as _re
    FONT = '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman" w:eastAsia="Times New Roman"/>'
    def set_spacing(xml, sid, line):
        pat = _re.compile(r'(<w:style [^>]*w:styleId="%s"[^>]*>)(.*?)(</w:style>)' % sid, _re.S)
        def fix(m):
            body = m.group(2)
            if '<w:pPr>' in body:
                body = _re.sub(r'(<w:pPr>)(.*?)(</w:pPr>)', lambda mm: mm.group(1) + _re.sub(r'<w:spacing[^>]*/>', '', mm.group(2)) + f'<w:spacing w:after="{120 if line == 240 else 180}" w:line="{line}" w:lineRule="auto"/>' + mm.group(3), body, count=1, flags=_re.S)
            else:
                body = _re.sub(r'(<w:name [^>]*/>(?:<w:basedOn [^>]*/>)?(?:<w:next [^>]*/>)?(?:<w:link [^>]*/>)?)', r'\1' + f'<w:pPr><w:spacing w:after="{120 if line == 240 else 180}" w:line="{line}" w:lineRule="auto"/></w:pPr>', body, count=1)
            return m.group(1) + body + m.group(3)
        return pat.sub(fix, xml, count=1)
    tmp = docx.with_suffix('.tmp.docx')
    with zipfile.ZipFile(docx) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == 'word/styles.xml':
                xml = data.decode('utf8')
                # fonts: replace theme fonts and any explicit rFonts with Times New Roman; 12pt default
                xml = _re.sub(r'<w:rFonts [^>]*/>', FONT, xml)
                if '<w:rPrDefault>' in xml:
                    xml = _re.sub(r'<w:rPrDefault>\s*<w:rPr>(.*?)</w:rPr>', lambda m: '<w:rPrDefault><w:rPr>' + FONT + _re.sub(r'<w:rFonts [^>]*/>|<w:sz [^>]*/>|<w:szCs [^>]*/>', '', m.group(1)) + '<w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>', xml, count=1, flags=_re.S)
                # default paragraph spacing 2.0
                if '<w:pPrDefault>' in xml:
                    xml = _re.sub(r'<w:pPrDefault>\s*<w:pPr>', '<w:pPrDefault><w:pPr><w:spacing w:line="480" w:lineRule="auto"/>', xml, count=1)
                    xml = xml.replace('<w:pPrDefault/>', '<w:pPrDefault><w:pPr><w:spacing w:line="480" w:lineRule="auto"/></w:pPr></w:pPrDefault>')
                else:
                    xml = xml.replace('<w:docDefaults>', '<w:docDefaults><w:pPrDefault><w:pPr><w:spacing w:line="480" w:lineRule="auto"/></w:pPr></w:pPrDefault>', 1)
                for sid in ('BodyText', 'FirstParagraph', 'Normal'):
                    xml = set_spacing(xml, sid, 480)
                for sid in ('FootnoteText', 'Footnote', 'Compact', 'TableCaption', 'ImageCaption', 'Caption', 'CaptionedFigure', 'Figure'):
                    xml = set_spacing(xml, sid, 240)
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
    print("    4. data/fig1_two_regimes.png … data/fig5_semantic_sequence.png (five figures)")
    print()


if __name__ == '__main__':
    main()
