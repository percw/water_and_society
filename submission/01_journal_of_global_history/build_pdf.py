#!/usr/bin/env python3
"""
JGH Submission PDF Builder
===========================
Generates a clean, typeset PDF of the submission manuscript.

Reads the compiled_manuscript.md, applies citation conversion + anonymization
(same pipeline as build_submission.py), then renders to PDF via weasyprint
with professional academic styling.

Usage:
    python build_pdf.py              # build manuscript PDF
    python build_pdf.py --all        # build manuscript + title page + cover letter

Requirements:
    pip install weasyprint markdown Pillow
"""

import re
import sys
import shutil
import tempfile
from pathlib import Path

try:
    import markdown
    from weasyprint import HTML
    from PIL import Image
except ImportError:
    print("ERROR: Missing dependencies. Install with:")
    print("  pip install weasyprint markdown Pillow")
    sys.exit(1)

# ── Paths ────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent.parent
PAPER_DIR = PROJECT_DIR / "archive" / "paper"
DATA_DIR = PROJECT_DIR / "data"

# ── Grayscale figure cache ────────────────────────────────────────────────────
BW_DIR = SCRIPT_DIR / "_bw_figures"


def ensure_grayscale(color_path: Path) -> Path:
    """Convert a color PNG to grayscale, caching in _bw_figures/."""
    BW_DIR.mkdir(exist_ok=True)
    bw_path = BW_DIR / color_path.name
    # Re-convert only if the source is newer
    if bw_path.exists() and bw_path.stat().st_mtime >= color_path.stat().st_mtime:
        return bw_path
    img = Image.open(color_path).convert('L')  # L = 8-bit grayscale
    img.save(bw_path, optimize=True)
    print(f"    ⬛ {color_path.name} → grayscale")
    return bw_path


# ── Import shared config from build_submission.py ────────────────────────────
sys.path.insert(0, str(SCRIPT_DIR))
from build_submission import BIBLIOGRAPHY, load_config, convert_to_footnotes


# ── CSS Stylesheet ───────────────────────────────────────────────────────────
ACADEMIC_CSS = """
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Source+Sans+3:wght@400;600;700&display=swap');

@page {
    size: A4;
    margin: 30mm 25mm 30mm 25mm;

    @top-center {
        content: "The Linguistic Hydro-Social Cycle";
        font-family: 'Source Sans 3', 'Helvetica Neue', sans-serif;
        font-size: 8pt;
        color: #999;
        padding-bottom: 6mm;
    }
    @bottom-center {
        content: counter(page);
        font-family: 'Source Sans 3', 'Helvetica Neue', sans-serif;
        font-size: 9pt;
        color: #666;
    }
}

@page :first {
    @top-center { content: none; }
}

* {
    box-sizing: border-box;
}

body {
    font-family: 'EB Garamond', 'Georgia', 'Times New Roman', serif;
    font-size: 12pt;
    line-height: 1.65;
    color: #1a1a1a;
    max-width: 100%;
    hyphens: auto;
    text-align: justify;
    orphans: 3;
    widows: 3;
}

/* ── Headings ─────────────────────────────────────────────────── */
h1 {
    font-family: 'Source Sans 3', 'Helvetica Neue', sans-serif;
    font-size: 22pt;
    font-weight: 700;
    color: #1a1a1a;
    margin-top: 0;
    margin-bottom: 8pt;
    line-height: 1.2;
    text-align: left;
    page-break-after: avoid;
}

h2 {
    font-family: 'Source Sans 3', 'Helvetica Neue', sans-serif;
    font-size: 14pt;
    font-weight: 600;
    color: #2c2c2c;
    margin-top: 24pt;
    margin-bottom: 8pt;
    line-height: 1.3;
    text-align: left;
    page-break-after: avoid;
}

h3 {
    font-family: 'Source Sans 3', 'Helvetica Neue', sans-serif;
    font-size: 12pt;
    font-weight: 600;
    color: #333;
    margin-top: 18pt;
    margin-bottom: 6pt;
    text-align: left;
    page-break-after: avoid;
}

/* ── Title block ──────────────────────────────────────────────── */
.title-block {
    text-align: center;
    margin-bottom: 36pt;
    padding-bottom: 18pt;
    border-bottom: 0.5pt solid #ccc;
}

.title-block h1 {
    font-size: 20pt;
    text-align: center;
    margin-bottom: 12pt;
}

.title-block .journal {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 10pt;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 1.5pt;
    margin-bottom: 6pt;
}

.title-block .meta {
    font-size: 10pt;
    color: #666;
    font-style: italic;
}

/* ── Abstract ─────────────────────────────────────────────────── */
.abstract {
    margin: 24pt 20pt;
    padding: 16pt 20pt;
    background: #f9f9f9;
    border-left: 3pt solid #666;
    font-size: 10.5pt;
    line-height: 1.55;
    text-align: justify;
}

.abstract-label {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 10pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1pt;
    color: #555;
    margin-bottom: 6pt;
    display: block;
}

/* ── Paragraphs ───────────────────────────────────────────────── */
p {
    margin-top: 0;
    margin-bottom: 10pt;
    text-indent: 0;
}

/* ── Tables ────────────────────────────────────────────────────── */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 16pt 0 20pt 0;
    font-size: 9.5pt;
    line-height: 1.4;
    page-break-inside: avoid;
}

thead {
    border-bottom: 2pt solid #333;
}

thead th {
    font-family: 'Source Sans 3', sans-serif;
    font-weight: 600;
    padding: 6pt 8pt;
    text-align: left;
    color: #333;
    border-bottom: 2pt solid #333;
    white-space: nowrap;
}

tbody td {
    padding: 4pt 8pt;
    border-bottom: 0.5pt solid #ddd;
}

tbody tr:last-child td {
    border-bottom: 1.5pt solid #333;
}

/* Bold rows in tables */
tbody td strong {
    font-weight: 700;
}

caption, .table-note {
    font-size: 9pt;
    color: #555;
    text-align: left;
    font-style: italic;
    margin-top: 4pt;
}

/* ── Figures ──────────────────────────────────────────────────── */
figure, .figure {
    margin: 20pt 0;
    text-align: center;
    page-break-inside: avoid;
}

img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 0 auto;
}

figcaption, em {
    /* em used for figure captions in the manuscript */
}

.fig-caption {
    font-size: 9.5pt;
    line-height: 1.45;
    color: #444;
    text-align: justify;
    margin-top: 8pt;
    padding: 0 12pt;
}

/* ── Footnotes ────────────────────────────────────────────────── */
.footnote-ref {
    font-size: 8pt;
    vertical-align: super;
    line-height: 0;
    color: #555;
    text-decoration: none;
}

.footnotes {
    margin-top: 30pt;
    padding-top: 12pt;
    border-top: 0.5pt solid #999;
    font-size: 9pt;
    line-height: 1.45;
    color: #444;
}

.footnotes ol {
    padding-left: 18pt;
}

.footnotes li {
    margin-bottom: 4pt;
}

.footnotes hr {
    display: none;
}

/* ── Horizontal rules ─────────────────────────────────────────── */
hr {
    border: none;
    border-top: 0.5pt solid #ccc;
    margin: 24pt 0;
}

/* ── Block quotes ─────────────────────────────────────────────── */
blockquote {
    margin: 12pt 20pt;
    padding-left: 12pt;
    border-left: 2pt solid #ccc;
    color: #555;
    font-style: italic;
}

/* ── Lists ────────────────────────────────────────────────────── */
ol, ul {
    margin: 8pt 0;
    padding-left: 24pt;
}

li {
    margin-bottom: 4pt;
}

/* ── Code / math ──────────────────────────────────────────────── */
code {
    font-family: 'SF Mono', 'Menlo', monospace;
    font-size: 9pt;
    background: #f4f4f4;
    padding: 1pt 3pt;
    border-radius: 2pt;
}

/* ── Print adjustments ────────────────────────────────────────── */
h1, h2, h3 {
    page-break-after: avoid;
}

table, figure, .figure {
    page-break-inside: avoid;
}

/* ── Data availability ────────────────────────────────────────── */
.data-availability {
    margin-top: 24pt;
    padding: 12pt 16pt;
    background: #fafafa;
    border: 0.5pt solid #ddd;
    font-size: 10pt;
}
"""


# ── Manuscript Processing ────────────────────────────────────────────────────

def process_manuscript(text: str) -> str:
    """Process the compiled manuscript markdown for PDF rendering."""

    # Strip the references section (footnotes replace inline citations)
    text = re.sub(r'\n# 8\. References.*?(?=\n# |\Z)', '', text, flags=re.DOTALL)

    # Convert inline citations to footnotes
    text = convert_to_footnotes(text)

    # Anonymize repository URLs
    text = text.replace(
        'https://github.com/percw/water_and_society',
        '[REPOSITORY URL REDACTED FOR REVIEW]'
    )
    text = text.replace('percw/water_and_society', '[REPOSITORY REDACTED]')

    # Fix LaTeX thousand separator
    text = text.replace('{,}', ',')

    # Fix image paths BEFORE math conversion — the subscript regex in
    # _latex_to_text will mangle underscores in filenames (e.g. did_figure_one
    # becomes did<sub>f</sub>igure<sub>o</sub>ne), so we must resolve and
    # replace <img> tags first.
    # We output HTML <img> tags (not markdown ![]()), because the images live
    # inside <div align="center"> blocks and markdown parsers ignore markdown
    # syntax inside raw HTML blocks.
    def fix_img(m):
        src = m.group(1)
        alt = m.group(2) if m.group(2) else ''
        # Resolve from paper dir (where compiled_manuscript.md lives)
        abs_path = (PAPER_DIR / src).resolve()
        if not abs_path.exists():
            # Also try from script dir
            abs_path = (SCRIPT_DIR / src).resolve()
        if abs_path.exists():
            bw = ensure_grayscale(abs_path)
            return f'<img src="{bw}" alt="{alt}" />'
        return m.group(0)

    text = re.sub(
        r'<img\s+src="([^"]+)"\s+alt="([^"]*)"\s*(?:width="[^"]*")?\s*/?>',
        fix_img, text
    )

    # Convert $...$ math to plain text for HTML rendering
    # Display math: $$ ... $$
    def display_math_to_text(m):
        content = m.group(1).strip()
        content = content.replace('\\\\', '\\')
        # Clean up LaTeX commands for plain text display
        content = _latex_to_text(content)
        return f'<div class="math-display" style="text-align:center; margin:12pt 0; font-style:italic; font-size:11pt;">{content}</div>'

    text = re.sub(r'\$\$(.*?)\$\$', display_math_to_text, text, flags=re.DOTALL)

    # Inline math: $...$ (single-line only — [^$\n]+? prevents spanning across
    # paragraph boundaries which would swallow figure blocks and other content)
    def inline_math_to_text(m):
        content = m.group(1)
        content = _latex_to_text(content)
        return f'<em>{content}</em>'

    text = re.sub(r'\$([^$\n]+?)\$', inline_math_to_text, text)

    # Convert <div align="center">...<em><strong>Figure N: ...</strong>...</em></div>
    # into proper figure + caption blocks
    def fix_figure_block(m):
        content = m.group(1)
        return content

    text = re.sub(
        r'<div\s+align="center">\s*(.*?)\s*</div>',
        fix_figure_block, text, flags=re.DOTALL
    )

    # Clean up <br> tags
    text = text.replace('<br>', '\n')

    return text


def _latex_to_text(latex: str) -> str:
    """Convert LaTeX math notation to readable plain-text/HTML."""
    s = latex
    # Greek letters
    greeks = {
        '\\alpha': 'α', '\\beta': 'β', '\\gamma': 'γ', '\\delta': 'δ',
        '\\epsilon': 'ε', '\\varepsilon': 'ε', '\\theta': 'θ',
        '\\hat{\\theta}': 'θ̂', '\\hat\\theta': 'θ̂',
    }
    for cmd, char in greeks.items():
        s = s.replace(cmd, char)

    # Operators and symbols
    s = s.replace('\\times', '×')
    s = s.replace('\\ge', '≥')
    s = s.replace('\\le', '≤')
    s = s.replace('\\approx', '≈')
    s = s.replace('\\neq', '≠')
    s = s.replace('\\sum', 'Σ')
    s = s.replace('\\mathbb{I}', '𝟙')
    s = s.replace('\\mathbf{1}', '𝟏')

    # \text{...} → plain text
    s = re.sub(r'\\text\{([^}]*)\}', r'\1', s)

    # Subscripts: _{...} → subscript text (just flatten for plain text)
    s = re.sub(r'_\{([^}]*)\}', r'<sub>\1</sub>', s)
    s = re.sub(r'_([a-zA-Z0-9])', r'<sub>\1</sub>', s)

    # Superscripts: ^{...}
    s = re.sub(r'\^\{([^}]*)\}', r'<sup>\1</sup>', s)

    # Remove remaining backslashes from simple commands
    s = re.sub(r'\\([a-zA-Z]+)', r'\1', s)

    return s


def extract_abstract(text: str) -> tuple:
    """Split the abstract from the rest of the manuscript."""
    # Find the abstract section
    m = re.match(r'# Abstract\s*\n+(.*?)\n+---', text, re.DOTALL)
    if m:
        abstract = m.group(1).strip()
        rest = text[m.end():].strip()
        return abstract, rest
    return None, text


def build_html(md_text: str, doc_type: str = 'manuscript') -> str:
    """Convert processed markdown to full HTML document."""

    if doc_type == 'manuscript':
        abstract, body = extract_abstract(md_text)
    else:
        abstract, body = None, md_text

    # Convert markdown to HTML
    md_extensions = ['tables', 'footnotes', 'smarty', 'attr_list']
    html_body = markdown.markdown(body, extensions=md_extensions)

    # Build the abstract block
    abstract_html = ''
    if abstract:
        abstract_rendered = markdown.markdown(abstract, extensions=md_extensions)
        abstract_html = f'''
        <div class="abstract">
            <span class="abstract-label">Abstract</span>
            {abstract_rendered}
        </div>
        '''

    # Title block
    if doc_type == 'manuscript':
        title_html = '''
        <div class="title-block">
            <h1>The Linguistic Hydro-Social Cycle:<br>Water Infrastructure as a Precondition<br>for British Industrialization</h1>
        </div>
        '''
    elif doc_type == 'title_page':
        title_html = ''
        html_body = f'<div>{html_body}</div>'
    else:
        title_html = ''

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <style>{ACADEMIC_CSS}</style>
</head>
<body>
    {title_html}
    {abstract_html}
    {html_body}
</body>
</html>"""

    return full_html


# ── PDF Generation ───────────────────────────────────────────────────────────

def generate_pdf(html: str, output_path: Path):
    """Render HTML to PDF via weasyprint."""
    doc = HTML(string=html, base_url=str(PROJECT_DIR))
    doc.write_pdf(str(output_path))
    kb = output_path.stat().st_size // 1024
    print(f"  ✅ {output_path.name}  ({kb} KB)")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    build_all = '--all' in sys.argv

    print()
    print("=" * 60)
    print("  JGH Submission PDF Builder")
    print("=" * 60)
    print()

    # 1. Manuscript PDF
    source = PAPER_DIR / "compiled_manuscript.md"
    if not source.exists():
        print(f"  ERROR: {source} not found. Run compile_paper.py first.")
        sys.exit(1)

    print("  Processing manuscript...")
    text = source.read_text()
    processed = process_manuscript(text)
    html = build_html(processed, doc_type='manuscript')

    out_pdf = SCRIPT_DIR / "manuscript_jgh.pdf"
    print("  Rendering PDF...")
    generate_pdf(html, out_pdf)

    # 2. Optional: title page + cover letter
    if build_all:
        print()
        print("  Building supplementary documents...")

        # Title page
        tp_path = SCRIPT_DIR / "title_page.md"
        if tp_path.exists():
            tp_text = tp_path.read_text()
            tp_html = build_html(tp_text, doc_type='title_page')
            generate_pdf(tp_html, SCRIPT_DIR / "title_page.pdf")

        # Cover letter
        cl_path = SCRIPT_DIR / "cover_letter.md"
        if cl_path.exists():
            cl_text = cl_path.read_text()
            cl_html = build_html(cl_text, doc_type='cover_letter')
            generate_pdf(cl_html, SCRIPT_DIR / "cover_letter.pdf")

    print()
    print("=" * 60)
    print("  ✅ PDF generation complete!")
    print("=" * 60)
    print()
    print(f"  Output: {out_pdf}")
    if build_all:
        print(f"          {SCRIPT_DIR / 'title_page.pdf'}")
        print(f"          {SCRIPT_DIR / 'cover_letter.pdf'}")
    print()


if __name__ == '__main__':
    main()
