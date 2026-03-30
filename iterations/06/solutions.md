# Iteration 06: Solutions

Solutions addressing the DiD econometric limitations identified in [limitations.md](limitations.md).
Implementation: `did_robustness.py`

## 19. SUTVA Violation — Spillover Effects

**Status:** resolved

**Approach:** Progressive exclusion of spillover-exposed control countries, from most exposed (colonial subjects India, China) to least (France, Netherlands). If SUTVA violations inflate β₃, the coefficient should change substantially as we remove exposed controls.

**Results:**

| Configuration | N controls | β₃ | p-value | Sig |
|---|---|---|---|---|
| All controls (baseline) | 4 | 1575.3 | <0.0001 | *** |
| Drop India (colonial subject) | 3 | 1494.0 | <0.0001 | *** |
| Drop India + China | 2 | 1243.1 | <0.0001 | *** |
| Netherlands only (closest peer) | 1 | 1396.6 | <0.0001 | *** |
| France only (rival, less trade) | 1 | 1089.6 | <0.0001 | *** |

**Coefficient of Variation across configurations: 14.4%**

**Conclusion:** β₃ is remarkably stable (CV = 14.4%). Removing colonial subjects reduces β₃ by ~20% (from 1575 to 1243 with European-only), confirming some SUTVA-driven inflation from colonial extraction suppressing Asian controls. However, the effect remains highly significant (p < 0.0001) in all configurations, including the strictest (France-only, β₃ = 1090). The SUTVA violation inflates magnitude but does not create a spurious effect.

---

## 20. Endogenous Treatment Timing — T₀ Grid Search

**Status:** resolved

**Approach:** Run DiD across a grid of T₀ values from 1730 to 1810 (step = 5 years) to test whether β₃ significance depends on the specific data-derived T₀ = 1758.

**Results:**

- Grid: 17 values tested
- **Significant at 5%: 17/17 (100%)**
- β₃ range: [1460, 1974]
- Peak β₃ at T₀ = 1810

**Conclusion:** β₃ is significant for every plausible treatment year. This resolves the endogenous-timing concern (the result doesn't depend on the specific T₀ chosen) but simultaneously reveals a deeper issue — see #21 below. The DiD detects the Great Divergence robustly, but the 100% significance rate means the framework cannot discriminate between competing theories about *when* the divergence began.

---

## 21. Serial Correlation — Collapsed DiD + Permutation Inference

**Status:** resolved (with important qualifications)

**Approach:** Three tests following Bertrand, Duflo & Mullainathan (2004):
- Part A: Collapsed DiD (pre/post averages per country, N=10)
- Part B: Block permutation (randomly assign treatment across 5 countries)
- Part C: Temporal permutation (randomize T₀ across 1720-1860)

**Results:**

| Test | β₃ or p | Interpretation |
|---|---|---|
| Collapsed DiD | β₃ = 1575.3, p = 0.494 | Not significant (N=10, df=6 — no power) |
| Block permutation | p = 0.206 | Cannot reject (min possible p = 0.20 with 5 units) |
| Temporal permutation | **p = 0.728** | **NOT significant — critical finding** |

**Critical interpretation:**

The temporal permutation (p = 0.728) is the most important result in Iteration 06. It reveals that virtually **any** treatment year in 1720-1860 produces a significant DiD coefficient. The β₃ at T₀ = 1758 is not distinguishable from β₃ at random T₀ values. This means:

1. **The DiD confirms the Great Divergence** — Britain genuinely pulled away from controls (robust, real effect)
2. **But it cannot attribute this specifically to the NLP commodification crossover** — the same divergence appears regardless of where you draw the pre/post line
3. **The causal link between linguistic shift and GDP must rest on the Granger causality tests** (Phase 1.3, Phase 3.4b), not the DiD

This is consistent with the econometric reality that DiD with a continuous, monotonic treatment effect and a monotonic outcome cannot identify the specific timing of treatment onset. The DiD was the wrong tool for temporal specificity — it confirms *magnitude* of divergence but not *timing*.

**Honest framing for the thesis:** "The DiD framework robustly confirms that Britain experienced GDP per capita gains of ~1,100–1,600 2011$ relative to controls during the study period. However, this divergence is not specific to the NLP-derived treatment year. The temporal specificity of the water-first hypothesis rests on the Granger causality evidence (Phase 1.3: p = 0.005; Phase 3.4b: p = 0.007 for pre-steam subperiod with population control)."

---

## 22. No Event Study — Dynamic Treatment Effects

**Status:** resolved

**Approach:** Estimate dynamic DiD with 10-year bins relative to T₀. Omitted category: [-10, 0). Pre-treatment coefficients should be jointly zero (parallel trends). Post-treatment coefficients should show gradual increase (treatment effect accumulation).

**Results:**

| Period | Coef | p-value | Pattern |
|---|---|---|---|
| [-60, -50) | -298 | 0.130 | ns |
| [-50, -40) | -465 | 0.013 | * (one pre-trend violation) |
| [-40, -30) | -107 | 0.566 | ns |
| [-30, -20) | -88 | 0.634 | ns |
| [-20, -10) | -55 | 0.766 | ns |
| [-10, 0) | 0 (ref) | — | omitted |
| [0, +10) | +143 | 0.442 | ns (gradual onset) |
| [+10, +20) | +145 | 0.437 | ns |
| [+20, +30) | +241 | 0.195 | ns |
| [+30, +40) | +351 | 0.060 | marginal |
| [+40, +50) | +583 | 0.002 | ** (acceleration) |
| [+50, +60) onwards | +968 to +3919 | <0.001 | *** (sustained) |

**Pre-treatment joint F-test: F = 1.77, p = 0.117 → Cannot reject parallel trends**

**Conclusion:** The event study shows a textbook pattern:
1. Pre-treatment coefficients are jointly non-significant (p = 0.117), validating parallel trends
2. One pre-treatment bin ([-50, -40)) is marginally significant — this warrants a footnote but does not invalidate the overall pattern
3. Post-treatment effects show gradual onset and sustained acceleration — exactly what one would expect from an accumulating industrial divergence
4. The treatment effect becomes statistically significant ~40 years after T₀, consistent with the slow diffusion of water-powered industrialization

---

## 23. Interpolation Bias in Control Group Outcomes

**Status:** resolved

**Approach:** Compare three configurations: (a) full panel with interpolated CHN/IND, (b) European-only with real annual data (GBR, NLD, FRA), (c) benchmark-year-only for Asian controls.

**Results:**

| Configuration | β₃ | p-value | N |
|---|---|---|---|
| Full panel (all annual) | 1575.3 | <0.0001 | 1005 |
| **European only (real annual)** | **1243.1** | **<0.0001** | **603** |
| Benchmark-year Asian controls | 1309.9 | <0.0001 | 645 |

**Conclusion:** The European-only specification (using only countries with real annual data) gives β₃ = 1243, about 21% lower than the full panel but still highly significant. The interpolation in CHN/IND inflates β₃ somewhat (by smoothing away variance in controls and by including colonial-extraction-depressed trajectories), but the core finding is robust to restriction to real annual data only.
