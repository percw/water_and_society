#!/usr/bin/env python3
"""
Build the submission package for the energy-history version of the paper.

  manuscript.md  ->  manuscript.docx, manuscript.pdf   (anonymised; Times 12, double-spaced body)
  title_page.docx/.pdf and cover_letter.docx/.pdf      (from author_config.ini, git-ignored;
                                                        placeholders if the file is missing)

Figures are read from data/. Word counts are printed for the journal form.

Usage:  pip install pypandoc_binary python-docx weasyprint && python build.py
"""
import configparser, re, shutil, tempfile
from datetime import date
from pathlib import Path

import pypandoc
from docx import Document
from docx.shared import Pt, RGBColor
from weasyprint import HTML

HERE = Path(__file__).resolve().parent
DATA = HERE.parent.parent / 'data'
MS = HERE / 'manuscript.md'
TITLE = "Floated before Fired: Canals, Coal and the Two Clocks of Britain's Energy Transition, 1700–1870"
REPO = 'https://github.com/percw/water_and_society'

CSS = """
@page { size: A4; margin: 2.5cm; @bottom-center { content: counter(page); font-size: 10pt; } }
body { font-family: 'Times New Roman', 'DejaVu Serif', serif; font-size: 12pt; line-height: 1.9; color: #000; }
h1 { font-size: 13pt; margin: 1.4em 0 .4em; } h2 { font-size: 12pt; font-style: italic; font-weight: normal; margin: 1em 0 .3em; }
header h1.title { font-size: 16pt; text-align: center; line-height: 1.3; margin-bottom: 1.5em; }
p { margin: 0 0 .6em; text-align: justify; }
table { border-collapse: collapse; font-size: 9.5pt; line-height: 1.3; margin: .5em 0 .3em; width: 100%; }
th, td { padding: 2px 5px; border-bottom: .5pt solid #999; } thead th { border-bottom: 1pt solid #000; }
img { max-width: 100%; } figure { margin: .5em 0 1.5em; page-break-inside: avoid; }
section.footnotes { font-size: 9.5pt; line-height: 1.35; } section.footnotes hr { display: none; }
"""


def words(md):
    """Words in text, notes and tables (figure files and markdown syntax excluded)."""
    md = re.sub(r'^---.*?---', '', md, flags=re.S)
    md = re.sub(r'!\[\]\([^)]*\)|\[\^\w+\]|\[(Figure|Table) \d+ about here\]', ' ', md)
    md = re.sub(r'[|:*#_\-]{2,}|[|*#]', ' ', md)
    return len(md.split())


def parts(md):
    body = md.split('# Tables')[0]; notes = '\n'.join(re.findall(r'^\[\^\w+\]: .*$', md, re.M))
    tables = md.split('# Tables')[1].split('\n[^')[0]
    abstract = md.split('# Abstract')[1].split('**Keywords')[0]
    text = body.split('# Introduction')[1]
    return {'abstract': words(abstract), 'text': words(text), 'notes': words(notes), 'tables_and_captions': words(tables)}


def style_docx(path, double=True):
    doc = Document(path)
    for st in doc.styles:
        try:
            f = st.font; f.name = 'Times New Roman'; f.color.rgb = RGBColor(0, 0, 0)
            if st.name.startswith('Heading') or st.name == 'Title': f.size = Pt(13 if st.name != 'Title' else 16); f.bold = True
        except (AttributeError, ValueError):
            pass
    for name in ['Normal', 'Body Text', 'First Paragraph', 'Compact', 'Abstract']:
        if name in [s.name for s in doc.styles]:
            s = doc.styles[name]; s.font.size = Pt(12)
            s.paragraph_format.line_spacing = 2.0 if double and name != 'Compact' else 1.0
    for name in ['Footnote Text', 'Table']:
        if name in [s.name for s in doc.styles]:
            s = doc.styles[name]; s.font.size = Pt(10); s.paragraph_format.line_spacing = 1.0
    doc.save(path)


def to_docx(md_path, out, double=True):
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / md_path.name; src.write_text(md_path.read_text())
        for f in DATA.glob('fig*.png'): shutil.copy(f, tmp)
        pypandoc.convert_file(str(src), 'docx', outputfile=str(out), extra_args=[f'--resource-path={tmp}'])
    style_docx(out, double)


def to_pdf(md_path, out):
    with tempfile.TemporaryDirectory() as tmp:
        for f in DATA.glob('fig*.png'): shutil.copy(f, tmp)
        html = pypandoc.convert_file(str(md_path), 'html5', extra_args=['--standalone', '--metadata', 'pagetitle=manuscript'])
        html = html.replace('</head>', f'<style>{CSS}</style></head>')
        HTML(string=html, base_url=tmp).write_pdf(out)


def config():
    cfg = {'author_name': 'Per Christian Wessel', 'email': 'per.c.wessel@gmail.com', 'affiliation': '[AFFILIATION]', 'postal_address': '[POSTAL ADDRESS]',
           'orcid': '[ORCID]', 'biography': '[BIOGRAPHY, max. 100 words]', 'acknowledgments': 'None.',
           'funding': 'This research received no specific grant from any funding agency, commercial or not-for-profit sectors.',
           'competing_interests': 'The author declares none.',
           'ai_declaration': ('Use of AI tools: the author used an AI assistant (Claude, Anthropic) to help write and debug the analysis code, '
                              'to check calculations and to edit the prose. The research question, interpretation and all conclusions are the '
                              "author's own; every number in the paper is produced by the public replication code.")}
    p = HERE / 'author_config.ini'
    if p.exists():
        c = configparser.ConfigParser(); c.read(p); cfg.update({k: v for k, v in c['author'].items() if v})
    return cfg


def title_page(cfg, wc):
    total = wc['text'] + wc['notes'] + wc['tables_and_captions']
    return f"""# Title page

*For editorial use only; not to be sent to reviewers.*

**{TITLE}**

{cfg['author_name']}
{cfg['affiliation']}
Postal address: {cfg['postal_address']}
Email: {cfg['email']}
ORCID: {cfg['orcid']}

**Word count.** {total:,} words including notes, tables and captions ({wc['text']:,} text, {wc['notes']:,} notes, {wc['tables_and_captions']:,} tables and captions); abstract {wc['abstract']} words. Four figures, four tables.

**Keywords.** energy transition; Industrial Revolution; canals; coal; water power; steam power; organic economy; growth regimes; text as data

**Author biography.** {cfg['biography']}

**Acknowledgements.** {cfg['acknowledgments']} {cfg['ai_declaration']}

**Funding.** {cfg['funding']}

**Competing interests.** {cfg['competing_interests']}

**Data availability.** All code and data are public at {REPO}; a self-contained replication package is supplied with the submission.
"""


WHY = {
    'energy': ('The article belongs in the *Journal of Energy History* because its subject is the chronology of an energy transition: it separates mineral heat from mineral power, dates each, and places water transport between them, and its closing check is addressed to energy historians working on infrastructure in other periods.'),
    'transport': ('The article belongs in the *Journal of Transport History* because its subject is what the canal network did in the first industrial economy: it builds a corrected annual series of canal openings, relates it to coal, population and income per head, and shows how far a national transport series can carry a claim about sequence, which bears on the recent quantitative work of Bogart, Satchell, Shaw-Taylor and co-authors.')}


def cover_letter(cfg, journal, wc, why):
    total = wc['text'] + wc['notes'] + wc['tables_and_captions']
    return f"""{date.today().strftime('%-d %B %Y')}

To the Editors, *{journal}*

Dear Editors,

I submit for consideration as a research article **'{TITLE}'** ({total:,} words including notes, tables and captions; four figures, four tables).

The article asks what powered Britain's economic acceleration of the 1770s and 1780s, a generation before the steam engine supplied a significant share of the country's power. On annual sectoral series for 1700–1870 it finds two clocks of the energy transition: an aggregate break in 1775–92, absorbed by population and carried by mineral heat, water power and water transport, and a per-capita break in 1818 that belongs to steam. Steam supplied 6% of installed power in 1760 and 21% in 1800, while coal output per head doubled. Coal and population rose with a corrected annual series of canal openings and income per head did not, and in the Google Books British corpus the vocabulary of coal on the water precedes the vocabulary of steam by a generation. The article engages directly with the Wrigley, Allen, Pomeranz and Malm debate on the fossil economy and with Tvedt's thesis that engineered water was its precondition.

The article is also explicit about the limits of its evidence. Randomisation inference and a timing placebo show that a slowly accumulated national stock such as a canal network cannot, on its own, show that its timing mattered; the sequence rests on break dates, power benchmarks and print. The same three-step check applies to any claim that infrastructure — canals, railways, grids, pipelines — was the precondition of an energy transition, which I hope makes the article useful beyond its case.

{WHY[why]}

{cfg['ai_declaration'].replace('Use of AI tools: the author', 'Use of AI tools. I', 1)}

An earlier and substantially different version of this analysis was submitted to the *Journal of Global History* and declined without review as outside the journal's scope. The present version is reframed, shortened and re-estimated on a corrected canal series. The manuscript has been anonymised; an earlier version of the analysis has been public in a code repository, which referees searching for the topic may encounter. It is not under consideration elsewhere. {cfg['competing_interests']} {cfg['funding']}

Yours sincerely,

{cfg['author_name']}
{cfg['affiliation']}
{cfg['email']}
"""


def main():
    md = MS.read_text(); wc = parts(md)
    print(f"Word count: abstract {wc['abstract']}, text {wc['text']}, notes {wc['notes']}, tables+captions {wc['tables_and_captions']}; "
          f"text+notes {wc['text'] + wc['notes']}; all {wc['text'] + wc['notes'] + wc['tables_and_captions']}")
    to_docx(MS, HERE / 'manuscript.docx'); to_pdf(MS, HERE / 'manuscript.pdf'); print('  manuscript.docx, manuscript.pdf')
    cfg = config()
    for name, text in [('title_page', title_page(cfg, wc)),
                       ('cover_letter', cover_letter(cfg, 'Journal of Energy History / Revue d’histoire de l’énergie', wc, 'energy')),
                       ('cover_letter_jth', cover_letter(cfg, 'The Journal of Transport History', wc, 'transport'))]:
        p = HERE / f'{name}.md'; p.write_text(text); to_docx(p, HERE / f'{name}.docx', double=False); to_pdf(p, HERE / f'{name}.pdf')
        print(f'  {name}.md/.docx/.pdf')


if __name__ == '__main__':
    main()
