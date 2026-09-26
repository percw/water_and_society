# Replication package

**Floated before Fired: Canals, Coal and the Two Clocks of Britain's Energy Transition, 1700–1870**

Every number, table and figure in the manuscript is produced by the code in this package from the
data in this package. Python 3.10+; `pip install -r requirements.txt`. Total run time is under two minutes.

## Run order

```bash
python code/canal_series_v2.py                   # corrected canal series  -> data/external/canal_cum_miles.csv
python code/regime_analysis.py    > output/results_regime.txt
python code/mechanism_analysis.py > output/results_mechanism.txt
python code/methods/identification_simulation.py > output/results_identification.txt
python code/methods/falsification.py > output/results_falsification.txt
python code/regime_figures.py                    # Figures 1, 2, 4
python code/methods/falsification_figure.py      # Figure 3
```

`code/fetch_external.py` re-downloads the Bank of England, Maddison and canal-list sources (about 35 MB)
and rebuilds the tidy CSVs; it is not needed to reproduce the paper.

## Where each result comes from

| Manuscript | Script | Output section |
|---|---|---|
| Table 1 (growth rates, break dates); 1818 break with war dummy | `regime_analysis.py` | §2 |
| Table 2 (power); steam crossover 1833; coal per steam hp | `mechanism_analysis.py` | §7 |
| Steam → income per head local projections | `mechanism_analysis.py` | §8 |
| Table 3 columns 1–2 | `regime_analysis.py` | §3 (a), (b) |
| Table 3 column 3 (first-difference sums) | `falsification.py` | D |
| Table 3 column 4, Figure 3 (b), randomisation p-values | `falsification.py` | E, C |
| Figure 3 (a), timing placebo | `falsification.py` | A |
| Predetermined doses (lagged stock, Priestley authorisations) | `mechanism_analysis.py` | §11–12 |
| Size-corrected threshold (p < 0.003); detectable effect (~40%) | `methods/identification_simulation.py` | — |
| Table 4, Figure 4 (print sequence) and robustness | `mechanism_analysis.py` | §10, §14 |
| 'canal' frequency vs stock (r = 0.91) | `regime_analysis.py` | §5 |
| Comparative benchmarks; war drawdowns | `regime_analysis.py` | §1, §4 |

## Data

| File | Content | Source |
|---|---|---|
| `data/external/boe_gb.csv` | GB sectoral output, population, 1700–1870 | Bank of England, *A Millennium of Macroeconomic Data* v3.1 (Broadberry et al. 2015) |
| `data/external/uk_canals_wiki.csv` | reference table of English waterways as retrieved 3 Sep 2026 | 'List of canals in the United Kingdom', Wikipedia |
| `data/external/canal_corrections.csv` | 24 documented corrections and additions, each with its reason | Hadfield, *The Canals of the British Isles*; Hadfield, *British Canals* |
| `data/external/uk_canals_v2.csv`, `canal_cum_miles.csv` | corrected table and cumulative miles (used in the paper) | built by `canal_series_v2.py` |
| `data/external/canal_cum_miles_v1.csv` | uncorrected cumulative miles, for comparison | |
| `data/external/priestley_1831_acts.csv` | first and last Act years for 152 navigations | parsed from Priestley (1831), archive.org OCR |
| `data/external/power_hp.csv` | installed steam, water and wind horsepower, 1760/1800/1830/1870 | Kanefsky (1979) via Crafts (2004) |
| `data/external/ngram_bigrams_coal_transport.csv`, `data/ngram_english.csv` | Google Books frequencies | Ngram Viewer, eng_gb_2019 |
| `data/external/mpd_panel.csv` | GDP per head and population, 13 countries | Maddison Project Database 2023 |

The canal corrections are the part of the data most open to improvement: a definitive series would use the
Cambridge Group's sectional opening dates. Results on the uncorrected table are the same in sign and similar in size
(`output/results_regime_v1_uncorrected.txt`).
