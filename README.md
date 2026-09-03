# Water Before Steam

[![Status: Working Paper](https://img.shields.io/badge/Status-Working--Paper-blue.svg)](#)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Canals, coal and the precondition for Britain's steam economy, 1700–1870.**

📖 [Compiled manuscript](archive/paper/compiled_manuscript.md) · 🧭 [Research strategy](docs/strategy_v2.md) · 📝 [Analysis memo, 3 September 2026](docs/memos/2026-09-03_canals_before_steam.html)

> Britain's industrial take-off is usually dated by steam. This project dates it by water. Using annual British sectoral output (Broadberry et al. 2015), a new year-by-year series of canal mileage, installed steam and water horsepower, the Maddison Project Database 2023 and the Google Books British corpus, we show that Britain passed through **two growth regimes**: an aggregate acceleration in 1775–1792 that ran on water and was absorbed by population, and a per-capita acceleration after 1818 that ran on steam. Canal mileage predicts coal output and population, not income per head. Steam raises income per head only after 1830. Water infrastructure was the precondition, in Tvedt's (2010) sense, that made a coal economy possible.

<div align="center">
  <img src="data/fig1_two_regimes.png" alt="Figure 1: Britain's two growth regimes" width="900">
</div>

---

## Findings

1. **Two regimes, not one.** Trend breaks in total output, industry, services, coal, iron and population fall between 1775 and 1792. Income per head breaks in 1818. Agriculture never breaks. Between 1760 and 1815 aggregate growth rose by about one percentage point a year and population growth by about one point; income per head kept growing at 0.3 per cent.
2. **Canals are a dose that predicts the right things.** Cumulative canal miles (155 canals, 2,967 miles; two waves, 1760–80 and 1790–1816, corroborated by 152 parliamentary authorisations parsed from Priestley 1831) predict coal output over 5–20 years in every specification, including quadratic trend and first differences, and predict population. They predict neither income per head nor agriculture.
3. **The chain runs water → coal → steam → income.** Local projections: canal stock raises coal within a decade and installed steam horsepower over 15–20 years; steam horsepower raises income per head only on samples extending past 1830. Steam overtook water and wind as a power source in 1833.
4. **Print agrees.** In the British corpus "coal barge" (1781) and "coal wharf" (1800) reach a quarter of their 1850 frequency a generation before "steam engine" (1808) and "steam power" (1826). The frequency of "canal" tracks the physical canal stock at r = 0.91 and the building rate not at all.
5. **The cross-country DiD was measuring the Napoleonic wars.** The 1761 treatment effect against France and the Netherlands (β₃ = 1,251, HAC p = 0.042) reproduces exactly and breaks in 1807, when Dutch income per head fell 44 per cent under French occupation. Britain fell 1.4 per cent. We withdraw the earlier estimate and its 47 per cent counterfactual and keep the analysis as a methodological caution.
6. **The aggregate divergence was pre-steam.** Between the Maddison benchmark years 1700 and 1820 Britain's total output grew 240 per cent, twice Germany's, while steam supplied at most a fifth of its power. The Netherlands, with Europe's densest waterways and no coal, grew 9 per cent.

---

## Repository layout

```
src/
  fetch_data.py          Google Books unigrams (71 terms) and Maddison cache        [original]
  fetch_external.py      Bank of England millennium data, Maddison 2023, canal list [new]
  regime_analysis.py     War confound, two regimes, canal dose, benchmarks, NLP proxy [new]
  mechanism_analysis.py  Horsepower, local projections, mediation, bigram sequencing [new]
  regime_figures.py      Figures 1–5 for the paper                                  [new]
  did_analysis.py        Cross-country DiD / event study / placebos (Section 4.6)   [original]
  dml_analysis.py        Cross-country DML (replication of the earlier version)     [original]
data/
  external/              Tidy CSVs: boe_gb, mpd_panel, uk_canals_wiki, canal_cum_miles,
                         power_hp, priestley_1831_acts, ngram_bigrams_coal_transport
  external/raw/          Downloaded xlsx and OCR text (git-ignored; fetch_external.py)
  fig1_…fig5_*.png       Paper figures
  did_*.png              Figures of the earlier version
docs/
  strategy_v2.md         Research strategy and order of work
  results_regime_v1.txt, results_mechanism_v1.txt   Frozen output of the two analysis scripts
  memos/                 Analysis memo (HTML) and its generator
archive/paper/           Manuscript sections 00–08 and compile_paper.py
submission/              Journal of Global History build scripts and replication package
```

## Reproduce

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/fetch_data.py                 # ngram unigrams + Maddison cache (uses embedded fallback offline)
python src/fetch_external.py             # Bank of England, Maddison 2023, canal list (~35 MB download)
python src/regime_analysis.py    | tee docs/results_regime_v1.txt
python src/mechanism_analysis.py | tee docs/results_mechanism_v1.txt
python src/regime_figures.py
python src/did_analysis.py               # earlier cross-country design, Section 4.6
cd archive/paper && python compile_paper.py
```

The two horsepower benchmark files and the canal table are small and committed; everything else regenerates.

## Sources

Broadberry, Campbell, Klein, Overton and van Leeuwen (2015) via the Bank of England *Millennium of Macroeconomic Data* v3.1 · Maddison Project Database 2023 (Bolt and van Zanden 2024) · Kanefsky (1979) horsepower via Crafts (2004) · Priestley (1831), *Historical Account of the Navigable Rivers, Canals, and Railways* (archive.org OCR) · Google Books Ngram, `eng_gb_2019` · canal completion table compiled from published reference lists.

## Citation

Working paper, September 2026. Please cite the repository until a preprint DOI is issued.
