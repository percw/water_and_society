# Strategy v2 — Canals as the precondition for coal-based industrialisation

*3 September 2026. Supersedes the identification strategy in the JGH submission draft. Evidence and charts: `docs/memos/2026-09-03_canals_before_steam.html`; numbers reproduce from `src/regime_analysis.py`.*

## The claim, stated the way Tvedt states it

Water infrastructure was not a rival to coal and was not "more important" than coal. It was the **necessary precondition** that made a coal economy possible in Britain and impossible elsewhere. Canals (and the improved rivers before them) moved coal from pithead to market, doubled coal use per head before any steam capacity existed, and shifted Britain from a per-capita to an aggregate growth regime in 1775–1792. Steam, from the 1820s, built on that base and produced the per-capita divergence. Tvedt's "why England and not China and India" is a claim about the *match* between water geography and coal geography; the Netherlands, with dense waterways and no coal, is the control case that shows water alone was not sufficient.

The empirical form of a precondition claim is **sequence plus dependence**, not a horse race. We test that canals came first, that coal output responded to the canal stock, that steam diffusion followed coal, and that per-capita growth followed steam. Rival vocabularies and rival sectors (agriculture) are the placebos.

## What we drop

- The binary 1761 DiD on GDP per capita and its 47% counterfactual. Britain's GDP per capita grew 0.08%/yr in 1760–1790; the 1807 break in the gap is the Dutch collapse under French occupation (−44%); pre-1751 event-study bins fail parallel trends once the Netherlands is removed. This design cannot recover a canal-era effect with any control group.
- Dual reporting of OLS and HAC as if they were the same table (Table 2 vs Table 3 in the draft).
- Any annual cross-country regression using Maddison population before 1820 (interpolated).

## Route: no GIS. Three pillars.

### Pillar 1 — Within-Britain regime shift and dose-response (core of the paper)

Data already in `data/external/`: Broadberry et al. sectoral output, population, capital stock (Bank of England); canal miles by completion year.

1. **Regime shift.** Slope-change tests at 1761 and data-chosen breaks (Quandt-Andrews, two-break) on total GDP, industry, coal, iron, services, population; GDP per capita and agriculture as pre-registered placebos. Result already in hand: canal-served series break 1775–1792, per-capita income breaks 1818, agriculture never.
2. **Dose-response.** Canal stock → coal, industry, population. Report levels-with-trend, quadratic trend, first differences and 10-year local projections side by side; coal is the robust channel and that is the one the mechanism predicts.
3. **Upgrade the dose series without GIS.** Replace the Wikipedia list with Joseph Priestley, *Historical Account of the Navigable Rivers, Canals, and Railways of Great Britain* (1831; public domain on archive.org / Google Books), which lists every navigation with length, Act year and opening. Add J. R. Ward, *The Finance of Canal Building in Eighteenth-Century England* (1974) for annual authorised capital 1755–1815. Both are tables, not maps.
4. **Steam as a real quantity.** Replace the "steam" ngram in the horse race with Kanefsky and Robey (1980) engine counts by decade (and Watt engine numbers from Tann). Interpolate to annual.

### Pillar 2 — The precondition chain (sequence and mediation)

1. **Local projections** canal stock → coal (5–20 year horizons), coal → steam engines, steam → GDP per capita. Already coded in `regime_analysis.py` section 6 with the ngram steam proxy; swap in engine counts.
2. **Mediation in the DML.** Treatment = canal stock (or Priestley mileage); mediator = coal output; outcome = industrial output / GDP per capita. The existing DML code needs only a new treatment column. The "water effect vanishes when steam is controlled" result becomes the *intended* finding: the effect runs through coal and steam.
3. **Necessary-not-sufficient test (comparative, no GIS).** Netherlands: densest waterway network in Europe by 1660 (de Vries 1978, *Barges and Capitalism*), no coal, no take-off. Britain: waterways + coalfields. Present as a 2×2 (water infrastructure × domestic coal) with Maddison benchmark years 1700/1820/1870 for NLD, GBR, FRA, BEL. Belgium, with coal and canals, industrialises first on the continent — that supports the interaction.

### Pillar 3 — Text as data, re-positioned as measurement

1. **Stock proxy.** The "canal" print frequency correlates 0.91 with the cumulative network and ~0 with miles opened per decade. Report this as validation: the vocabulary index measures infrastructure in place. That reframes the 1766 crossover as the corpus registering the first wave of openings, not the acts.
2. **Semantic sequencing of coal.** Using the existing bigram/co-occurrence data: does "coal" co-occur with canal/navigation/wharf/barge before it co-occurs with engine/steam/boiler? Expected: yes, by 20–40 years. This is the linguistic image of "the fossil economy was floated before it was driven".
3. **Placebo vocabularies** retained (textiles, finance, agriculture) but now tested against sectoral output series rather than GDP per capita.

## Cross-country evidence, honestly bounded

Keep Maddison, but only: (a) benchmark-year growth 1700→1820 (Britain total GDP +240%, next best Germany +124%, and Britain alone raises income per head as well); (b) the war-drawdown table as an explicit confound; (c) the 1818 per-capita break as the steam-era result. Cite Crouzet (1964) on wartime economic change.

## Manuscript changes

- Title: *Canals, Coal and the Precondition for Steam: Water Infrastructure and Britain's Two Growth Regimes, 1700–1870* (working).
- Outcome variables: sectoral output and population, not GDP per capita, in the core sections.
- Fix citations: Bolt & van Zanden 2024 (JoES, 10.1111/joes.12618) for MPD 2023; Bogart 2014 chapter (not 2024 book); add Turnbull 1987 (EcHR 40:4), Alvarez-Palau, Bogart, Satchell & Shaw-Taylor 2024 (EJ), de Vries 1978, Kanefsky & Robey 1980, Priestley 1831, Ward 1974, Crouzet 1964.
- Journal: still *Journal of Global History*. The reframed thesis is a direct quantitative test of Tvedt (2010), published there.

## Order of work (status, 3 September 2026)

1. ✅ `src/fetch_external.py`, `src/regime_analysis.py`; frozen in `docs/results_regime_v1.txt`.
2. ◐ Priestley (1831): authorisation years parsed for 152 navigations (`priestley_1831_acts.csv`) and used as corroboration. Lengths not transcribed; the Wikipedia completion table remains the dose. Full transcription is the next data task.
3. ◐ Steam measured as Kanefsky (1979)/Crafts (2004) horsepower benchmarks, log-interpolated (`power_hp.csv`). Kanefsky–Robey engine counts by decade still to add.
4. ✅ Coal-by-water vs coal-by-steam bigram sequencing (`mechanism_analysis.py` §10, Figure 5, Table 5).
5. ✅ Decided against DML for the within-Britain series (over-fits trend on 130 obs); linear local projections used; mediation reported as a negative result (§9).
6. ✅ Manuscript rewritten (all sections), six new figures, seven tables, references verified via Crossref, JGH build scripts and replication package updated.
7. ☐ Next: county panel with CAMPOP waterways + coal deposits for cross-sectional identification (requires GIS or the Cambridge Group's tabulated data); author biography for the JGH title page; double spacing in Word.
