# Replication Package

## "The Linguistic Hydro-Social Cycle: Water Infrastructure as a Necessary Precondition for British Industrial Divergence"

---

### Overview

This replication package contains all code, data sources, and instructions necessary to reproduce every table, figure, and statistical result reported in the manuscript. The package is designed to satisfy the replication policies of *Explorations in Economic History* (Elsevier), *Cliometrica* (Springer), and *Journal of Global History* (Cambridge UP).

---

### System Requirements

| Component | Version |
|-----------|---------|
| Python | 3.10+ |
| Operating System | macOS, Linux, or Windows |
| Pandoc | 2.x+ (optional, for LaTeX compilation) |

### Python Dependencies

All dependencies are listed in `requirements.txt` at the repository root:

```
pandas
numpy
matplotlib
scikit-learn
gensim
statsmodels
scipy
requests
openpyxl
jupyter
```

---

### Replication Instructions

#### Step 1: Environment Setup

```bash
git clone https://github.com/percw/water_and_society.git
cd water_and_society
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
# .venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

#### Step 2: Data Acquisition

```bash
python src/fetch_data.py --force
```

This script fetches:
1. **Google Books Ngram Corpus** (`eng_gb_2019`): Annual frequency data for 71 vocabulary terms (1700–1900), covering hydro-infrastructure, fossil/steam, agrarian, canal transport, and placebo categories.
2. **Maddison Project Database 2023** (Bolt & van Zanden 2024): Annual GDP per capita estimates for Great Britain, France, the Netherlands, China, and India.

When network access is unavailable, the script uses comprehensive embedded fallback data sourced from the published databases, ensuring full offline reproducibility.

**Output:** Cached JSON files in `data/` and summary CSVs (`ngram_english.csv`, `maddison_gdp.csv`).

#### Step 3: Econometric Analysis

```bash
python src/did_analysis.py
```

This script executes the full analysis pipeline:

| Specification | Description | Output |
|:---|:---|:---|
| 1–9 | Baseline DiD suite (OLS, FE, HAC, log-GDP, extended controls) | `docs/results.txt` |
| 10 | Dynamic event study (5-year bins) | `data/did_event_study.png` (Figure 2) |
| 11 | Placebo-in-Space (treatment assigned to each control) | `docs/results.txt` |
| 12 | Randomization inference (permutation of treatment) | `data/did_permutation_test.png` |
| 13 | Sub-period DiD (pre-steam 1700–1810 vs. steam era 1810–1900) | `docs/results.txt` |
| 14 | Formal pre-trends test (slope = 0 in pre-period) | `docs/results.txt` |
| — | Channel decomposition (transport vs. fossil) | `data/did_channel_decomposition.png` |
| — | Collapsed DiD (Bertrand et al. 2004) | `docs/results.txt` |
| — | Clustered standard errors (country-level) | `docs/results.txt` |
| — | Figure 1 (NLP crossover + GDP divergence) | `data/did_figure_one.png` |
| — | Placebo vocabulary tournament | `data/did_vocab_tournament.png` (Figure 3) |

**Optional override:** Use `--t0 YEAR` to change the treatment year (default: derived from NLP crossover, anchored at 1761 for the Bridgewater Canal specification).

#### Step 4: Manuscript Compilation (Optional)

```bash
cd archive/paper
python compile_paper.py
```

Generates:
- `compiled_manuscript.md` — Markdown version
- `compiled_manuscript.tex` — LaTeX version (requires Pandoc)

---

### Data Sources

| Dataset | Source | Access |
|:---|:---|:---|
| Google Books Ngram (eng_gb_2019) | Google Books Ngram Viewer | https://books.google.com/ngrams |
| Maddison Project Database 2023 | Bolt & van Zanden (2024) | https://www.rug.nl/ggdc/historicaldevelopment/maddison/ |
| British population (1700–1900) | Wrigley & Schofield (1981); Mitchell (1988) | Embedded in `fetch_data.py` |

All original data sources are publicly available. The `fetch_data.py` script contains embedded benchmark values from the published databases to ensure full reproducibility even without network access.

---

### Output File Map

```
data/
├── maddison_gdp.csv                 # GDP per capita panel (GBR, FRA, NLD, CHN, IND)
├── ngram_english.csv                # Ngram frequency matrix (71 terms × 201 years)
├── did_figure_one.png               # Figure 1: NLP crossover + GDP divergence
├── did_event_study.png              # Figure 2: Dynamic event study
├── did_vocab_tournament.png         # Figure 3: Placebo vocabulary falsification
├── did_channel_decomposition.png    # Channel decomposition (transport vs. fossil)
├── did_parallel_trends.png          # Parallel trends validation
├── did_permutation_test.png         # Randomization inference histogram
├── did_regression_results.png       # Regression coefficient visualization
├── did_subperiod.png                # Sub-period DiD results
├── did_phase_portrait.png           # Phase portrait
└── did_vocabulary_did.png           # Vocabulary-based DiD

docs/
└── results.txt                      # Full numerical output (all specifications)

archive/paper/
├── compiled_manuscript.md           # Compiled manuscript (Markdown)
└── compiled_manuscript.tex          # Compiled manuscript (LaTeX)
```

---

### Correspondence Between Manuscript and Code

| Manuscript Element | Script | Function / Line |
|:---|:---|:---|
| Table 1 (Summary Statistics) | `did_analysis.py` | `run_all_specifications()` |
| Table 2 (DiD Regression) | `did_analysis.py` | `run_all_specifications()` → Spec 3 (HAC) |
| Table 3 (Serial Autocorrelation) | `did_analysis.py` | `run_collapsed_did()`, `run_clustered_se()` |
| Figure 1 (NLP + GDP) | `did_analysis.py` | `generate_figure_one()` |
| Figure 2 (Event Study) | `did_analysis.py` | Event study specification (#10) |
| Figure 3 (Placebo Tournament) | `did_analysis.py` | `run_vocab_falsification_tournament()` |
| 47% pre-steam gap | `did_analysis.py` | `calculate_pre_steam_gap()` |
| 1766 crossover year | `fetch_data.py` | NLP crossover calculation |

---

### Software and Computation

All analysis was conducted in Python 3.10. Estimated runtime on a modern laptop:
- Data acquisition: ~2 minutes (with network) / <5 seconds (embedded fallback)
- Full econometric pipeline: ~30 seconds
- Manuscript compilation: <5 seconds

---

### Contact

For questions regarding replication, please contact the corresponding author.
