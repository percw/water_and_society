# Research Findings 02: Two growth regimes and the precondition chain

*3 September 2026. Supersedes `research_findings_01.md`. Numbers reproduce from `src/regime_analysis.py` and `src/mechanism_analysis.py`; frozen output in `docs/results_regime_v1.txt` and `docs/results_mechanism_v1.txt`.*

## Summary

The earlier finding (a 1761 cross-country DiD effect of 1,251 international dollars, 47% of the 1900 lead established by 1810) is an artefact of the Napoleonic collapse of the control group and has been withdrawn. In its place the project now documents:

1. **Two British growth regimes.** Aggregate output, industry, services, coal, iron and population break trend in 1775–1792; GDP per head breaks in 1818; agriculture never breaks. Between 1760 and 1815 aggregate growth and population growth each rose by about one percentage point per year while GDP per head kept growing at 0.3%.
2. **Canal mileage as a dose.** 155 canals, 2,967 miles, two waves (1760–80; 1790–1816). Cumulative miles predict coal output in every specification (linear trend +47%, quadratic trend +30%, first differences +27% per 1,000 miles, all p ≤ 0.001), predict population, and predict neither GDP per head nor agriculture. 152 Priestley (1831) authorisations independently show the 1790s peak (30 of 70 canals).
3. **The chain.** Local projections: canal stock → coal within 5–10 years; canal stock → steam horsepower over 15–20 years; steam horsepower → GDP per head only on the 1760–1870 sample, not 1760–1830. Steam overtook water and wind as stationary power in 1833. Coal output per head doubled 1700–1790 while steam supplied under a fifth of power.
4. **Semantic sequence.** "coal barge" reaches 25% of its 1850 frequency in 1781, "coal wharf" in 1800, "steam engine" in 1808, "steam power" in 1826. "steam engine" overtakes "fire engine" in 1800. "canal" frequency correlates 0.91 with the canal stock and −0.04 with miles opened per decade.
5. **War confound.** GDP per head drawdowns 1785–1815: Netherlands −44%, Portugal −48%, Sweden −27%, France −22%, Britain −1.4%. The Britain–controls gap breaks in 1807. Changing controls does not help: Britain's own GDP per head grew 0.08%/yr in 1760–1790.
6. **Benchmarks.** 1700→1820 total GDP: Britain +240%, Germany +124%, France +50%, Netherlands +9%. Britain alone combined population growth of +148% with GDP per head growth of +37%.

## Negative results kept on record

- Linear mediation (canal → coal → outcome) with quadratic trend: all paths' bootstrap intervals span zero; not identified on 130 observations.
- Reverse causality: past 10-year growth in coal, GDP and population predicts canal openings (p = 0.002–0.03). The dose is endogenous; the evidence is about sequence and incidence.
- Agriculture responds negatively to canal stock at 10–15 years (composition effect), so it is an imperfect placebo; GDP per head is the clean one.
- DML with tree learners is unusable within a single national time series (collapses treatment residual); retained only for the cross-country panel.

## Data added

`data/external/`: `boe_gb.csv` (Broadberry et al. via Bank of England), `mpd_panel.csv` (Maddison 2023), `uk_canals_wiki.csv` + `canal_cum_miles.csv`, `priestley_1831_acts.csv`, `power_hp.csv` (Kanefsky 1979 via Crafts 2004, Table 3; verified), `ngram_bigrams_coal_transport.csv` (16 bigrams), `lp_irfs.csv`, `semantic_sequence.csv`.

## Open items

See `docs/strategy_v2.md` and TRACKER items 24–25: engine counts by decade to replace interpolated horsepower; Priestley lengths for a definitive dose series; county panel with the CAMPOP waterways dataset for cross-sectional identification.
