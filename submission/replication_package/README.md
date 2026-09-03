# Replication Package

## "Water Before Steam: Canals, Coal and the Making of Britain's Fossil Economy, 1700–1870"

---

### Overview

This package contains the code, tidy data and instructions needed to reproduce every table, figure and statistic in the manuscript, plus the cross-country difference-in-differences of the earlier version that Section 4.6 of the paper discusses.

### System requirements

| Component | Version |
|---|---|
| Python | 3.10+ |
| Pandoc | 2.x+ (only for manuscript compilation) |

Python dependencies (`requirements.txt`): pandas, numpy, matplotlib, scikit-learn, statsmodels, scipy, requests, openpyxl.

### Structure

```
code/
  fetch_data.py            Google Books unigrams (71 terms), Maddison cache
  fetch_external.py        Bank of England millennium data, Maddison 2023, canal list -> data/external/*.csv
  regime_analysis.py       Sections 4.1, 4.2, 4.6, 4.7 and the NLP-stock result (Tables 1–3, 6, 7)
  mechanism_analysis.py    Sections 4.3–4.5 (Table 4, 5; Figure 3 inputs; mediation negative result)
  regime_figures.py        Figures 1–5
  did_analysis.py          Earlier-version cross-country DiD, event study, placebos
  dml_analysis.py          Earlier-version cross-country DML
data/
  maddison_real_gdp.csv, ngram_english.csv          inputs of the earlier version
  external/boe_gb.csv                               Broadberry et al. (2015) via Bank of England
  external/mpd_panel.csv                            Maddison 2023, 13 countries, log-interpolated
  external/uk_canals_wiki.csv, canal_cum_miles.csv  canal completion table and cumulative miles
  external/priestley_1831_acts.csv                  parliamentary authorisations parsed from Priestley (1831)
  external/power_hp.csv                             Kanefsky (1979) horsepower via Crafts (2004)
  external/ngram_bigrams_coal_transport.csv         16 bigrams, eng_gb_2019
  external/lp_irfs.csv, semantic_sequence.csv       intermediate outputs
figures/                                            all figures
output/                                             frozen logs of the three analysis scripts
manuscript/                                         compiled manuscript (Markdown and LaTeX)
```

### Steps

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python code/fetch_data.py                # uses embedded fallback if the Ngram API is unavailable
python code/fetch_external.py            # downloads ~35 MB (Bank of England xlsx, Maddison xlsx, Wikipedia wikitext)
python code/regime_analysis.py    | tee output/results_regime_v1.txt
python code/mechanism_analysis.py | tee output/results_mechanism_v1.txt
python code/regime_figures.py
python code/did_analysis.py              # earlier design, Section 4.6
```

Scripts expect the repository layout (`src/`, `data/`); when running from this package, copy `code/` to `src/` or run from a clone of the repository.

### Mapping from paper to output

| Paper | Script section | Output |
|---|---|---|
| Table 1, Table 2, Figure 1 | regime_analysis §2 | results_regime_v1.txt |
| Table 3, Figure 2 | regime_analysis §3 | results_regime_v1.txt |
| Figure 3, §4.3 | mechanism_analysis §8 | results_mechanism_v1.txt, lp_irfs.csv |
| Table 4 | mechanism_analysis §7 | results_mechanism_v1.txt |
| Table 5, Figure 5 | mechanism_analysis §10 | results_mechanism_v1.txt, semantic_sequence.csv |
| Table 6, Figure 4, §4.6 | regime_analysis §1; did_analysis.py | results_regime_v1.txt; results_earlier_version_did.txt |
| Table 7 | regime_analysis §4 | results_regime_v1.txt |
| NLP stock correlation (§4.5) | regime_analysis §5 | results_regime_v1.txt |
| Mediation (negative result, §3.5) | mechanism_analysis §9 | results_mechanism_v1.txt |

### Known provisional inputs

- `power_hp.csv` benchmark values are from Crafts (2004), Table 3, citing Kanefsky (1979a, p. 338); verified against the LSE working-paper version (WP 75/03).
- The canal table is compiled from published reference lists and dated by completion year; see paper §7.2.
- `priestley_1831_acts.csv` comes from OCR of the archive.org scan and covers 152 of roughly 300 entries.

### Licence

Code: MIT. Data: as licensed by the original providers (Bank of England, Maddison Project, Google Books, Wikipedia CC BY-SA).
