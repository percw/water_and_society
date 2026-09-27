# Pre-analysis plan: water, coal and the two clocks in space

**Status:** written and committed on 27 September 2026, before any of the spatial data below has
been downloaded or inspected. The git commit hash and date are the registration. Deviations will
be reported as deviations.

## Why a spatial design

The national series cannot tell whether the canals' *timing* mattered: the canal stock is 97.7% a
quadratic trend, stocks with the same waves moved to other decades fit coal about a third of the
time (randomisation p = 0.34), and canals not yet open fit coal as well as canals already open
(`docs/results_falsification_v2.txt`). Identification has to come from *where* and *when* individual
places were connected, not from one national time series.

## What already exists, and what is new here

| Work | What it does | What it leaves open |
|---|---|---|
| Alvarez-Palau, Bogart, Satchell and Shaw-Taylor (2025, *EJ*) | Market access 1680 and 1830 → growth of 458 towns | Two cross-sections; no timing, no coal complementarity |
| Bogart, Satchell, Shaw-Taylor et al. (2017 WP), turnpikes and canals | Waterway access c.1800 → parish population growth 1801–51 | Access fixed at one date; no event study; no coal interaction |
| Bogart, Bottomley, Satchell and Shaw-Taylor (2017 WP), steam engines | 1770 network → steam-engine adoption 1770–1800 | Network fixed at 1770; no staggered connection |
| Allen (2023, *JEH*) | Coal prices 1695/1795/1842 → transport productivity; "surprisingly limited impact on the geography of production and consumption" | Whether connection moved local coal prices and whether that moved people and engines |
| This project | Staggered connection year for every unit from the dynamic waterways GIS; event studies with clean controls; water × coal interaction; macro bridge back to the national regimes | |

The claim to novelty is narrow and testable: **the timing of connection, its interaction with coal,
and the aggregation back to the national two-regime chronology.**

## The three analyses

### 1. Timing: does connection *precede* growth? (event study)

- **Units and outcome A (annual):** the 404 Wrigley–Schofield reconstitution parishes, annual
  baptisms 1700–1837 (log, three-year centred mean). Annual data give 20+ pre-years for every
  connection cohort 1760–1830.
- **Units and outcome B (decennial):** all c. 9,000–12,600 census parish units, log population
  1801–1851; cohorts connected 1801–1841 only (earlier connections are always-treated and dropped
  from the control pool).
- **Treatment:** year a unit is first within **5 km** of a navigable waterway that is open in that
  year, from the dynamic GIS. Units already within 5 km of navigable water in 1700 are excluded
  from both treated and control sets (they are a different population).
- **Estimator:** stacked event study, clean controls = never connected or connected more than 20
  years later; unit×stack and year×stack fixed effects; SE clustered by unit (`src/spatial/estimators.py`).
  Window −10 to +20 (A), −2 to +4 decades (B).
- **Pre-registered tests:** (i) joint pre-trend test over e = −10…−2 (A) or −2 decades (B);
  (ii) mean effect over e = +10…+20 (A) or +2…+4 decades (B).
- **Robustness (all reported whatever they show):** 3 and 10 km thresholds; Sun–Abraham
  interaction-weighted estimator; dropping each canal-mania cohort 1790–1797 in turn; county×year
  fixed effects; a **terrain instrument**: the least-cost canal route cost from elevation and slope
  between each unit and the nearest pre-1760 navigable water (Tvedt's hydrology as the exogenous
  source of connection timing), reported as reduced form and 2SLS.
- **Falsification:** placebo connection dates drawn from the same cohort distribution (500 draws);
  *authorised-but-never-built* canals (Priestley's Acts that produced no canal) as placebo
  treatment on the date of the Act.

### 2. Complementarity: water × coal (Tvedt's matching rule, tested within Britain)

- **Moderator:** unit lies within **15 km of an exposed coalfield** (Satchell and Shaw-Taylor
  coalfield GIS), or the new link connects the unit to such a coalfield by water within 50 km
  (network distance). Pre-specified primary moderator: the network one.
- **Prediction if Tvedt is right:** the effect in analysis 1 is concentrated in connections that
  link to coal, and close to zero for connections that do not (the southern agricultural canals:
  Kennet and Avon, Basingstoke, Andover, Wilts and Berks, Royal Military are the natural cases).
- **Prediction if Tvedt is wrong:** similar effects with and without coal (connection as generic
  market access, as in Alvarez-Palau et al.).
- **Mechanism check:** delivered coal price in Allen's 1695, 1795 and 1842 cross-sections, as a
  long-difference regression of the log price change on connection between the dates, with and
  without the coal link. This tests Allen's "limited impact" directly.
- **Pre-registered test:** the difference between the coal-linked and non-coal event paths over
  e = +10…+20, and its sign.

### 3. The chain and the macro bridge

- **Steam:** engines erected per unit from the Early Engine Database (c. 2,950 engines to 1800,
  year and location). Event study of the cumulative number of engines (inverse hyperbolic sine)
  around connection, split by coal link. The chain predicts engines rise **after** connection and
  **only** where the connection links to coal.
- **Macro bridge:** `national_counterfactual()` removes the estimated connection effect from every
  connected unit and re-aggregates. It reports the share of England's population growth 1761–1831
  attributable to connection, and compares the timing of the counterfactual with the 1775–92
  national break. The two-clocks thesis predicts a substantial share for population and the
  aggregate, and none for income per head. (Local income is not observed; the occupational
  structure of the 1813–20 baptism registers, secondary-sector share, is the pre-specified proxy
  where it can be matched.)

## What would count against the thesis

Any of the following will be reported as the headline if found:

- flat post-connection paths (no effect of connection on growth);
- pre-trends of the same size as post-trends (canals followed growth, as the national reverse
  regressions suggest);
- equal effects with and without a coal link (no complementarity);
- engines not rising after connection, or rising equally without coal.

## Data manifest

See [`DATA_MANIFEST.md`](DATA_MANIFEST.md).
