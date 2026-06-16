# Iteration 06: Limitations of the Difference-in-Differences Causal Identification

**Reviewer:** Self-assessment (Econometric Methods Audit)
**Date:** 2026-03-29

This iteration identifies five fundamental econometric violations in the DiD causal identification framework (`did_analysis.py` v2) that, if left unaddressed, substantially weaken the causal claims of the thesis.

## 19. SUTVA Violation — Spillover Effects Across Treatment and Control Units

**The Weak Link:** The DiD framework assumes the Stable Unit Treatment Value Assumption (SUTVA): the treatment applied to Britain must not affect the outcomes of the control countries (NLD, FRA, CHN, IND).

**The Fatal Flaw:** Britain's industrialization profoundly affected every control country's GDP trajectory. The Netherlands and France were direct trading partners and military rivals whose economies co-moved with Britain through mercantilist competition. China and India were subject to British colonial extraction — India's GDP per capita *declined* partly *because* of British industrial ascendancy (Parthasarathi 2011; Broadberry et al. 2015). The DiD coefficient beta_3 therefore captures not just Britain's divergence upward, but also the controls' suppression downward — double-counting the "treatment effect" and inflating the estimator.

**References:**
- Rubin (1980), "Randomization Analysis of Experimental Data: The Fisher Randomization Test" — original SUTVA formulation
- Parthasarathi (2011), *Why Europe Grew Rich and Asia Did Not*
- Broadberry, Custodis & Gupta (2015), "India and the Great Divergence"

## 20. Endogenous Treatment Timing — Circularity in T_0 Derivation

**The Weak Link:** The treatment year T_0 is derived endogenously from the NLP commodification ratio (Industrial/Agrarian > 0.5), which is the same linguistic data that motivates the hypothesis.

**The Fatal Flaw:** Using the outcome-adjacent data to select the treatment cutoff introduces specification search bias and data-dependent inference (Leamer 1983). If T_0 were derived from an external, independent source (e.g., a key legislative act, patent date, or engineering milestone), the inference would be clean. But deriving it from the very Ngram frequencies that define the "hydro-social shift" creates circularity — the treatment timing is optimized (perhaps inadvertently) to maximize the divergence signal. Any sensitivity analysis must show that beta_3 is robust across a wide grid of plausible T_0 values, not just the data-selected optimum.

**References:**
- Leamer (1983), "Let's Take the Con out of Econometrics"
- Angrist & Pischke (2009), Ch. 5 on exogenous vs endogenous treatment assignment

## 21. Serial Correlation — Severely Inflated t-Statistics (Bertrand et al. 2004)

**The Weak Link:** The DiD panel contains 201 time periods (1700-1900, annual) with GDP per capita that is highly serially autocorrelated. The current implementation uses OLS with Newey-West HAC (maxlags=10) as only one robustness check.

**The Fatal Flaw:** Bertrand, Duflo & Mullainathan (2004) demonstrated that standard DiD with many time periods and serially correlated outcomes produces rejection rates of 45% when the true rate should be 5%. Newey-West with an arbitrarily chosen lag length is insufficient. The canonical solution is to cluster standard errors at the unit (country) level. However, with only N=5 clusters, cluster-robust SEs are also unreliable (Cameron, Gelbach & Miller 2008). The proper approach requires either: (a) wild cluster bootstrap, (b) collapsing the panel to pre/post averages, or (c) permutation inference — all of which may substantially reduce the statistical significance currently reported.

**References:**
- Bertrand, Duflo & Mullainathan (2004), "How Much Should We Trust Differences-in-Differences Estimates?"
- Cameron, Gelbach & Miller (2008), "Bootstrap-Based Improvements for Inference with Clustered Errors"

## 22. No Event Study — Missing Dynamic Treatment Effects

**The Weak Link:** Modern DiD practice requires an event-study specification with leads and lags to validate the parallel trends assumption dynamically and to show how the treatment effect evolves over time.

**The Fatal Flaw:** The current implementation tests only a single pre/post break at T_0. It does not estimate dynamic treatment effects (i.e., coefficients for each period relative to treatment). Without an event study: (a) the parallel trends assumption cannot be formally tested — the visual plot in Panel C is suggestive but not a statistical test; (b) the reader cannot see whether the treatment effect is immediate or gradual; (c) pre-treatment coefficients should be jointly zero if parallel trends hold. Modern DiD literature (Goodman-Bacon 2021; Sun & Abraham 2021; Callaway & Sant'Anna 2021) considers the event study specification essential for credibility.

**References:**
- Goodman-Bacon (2021), "Difference-in-Differences with Variation in Treatment Timing"
- Sun & Abraham (2021), "Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects"
- Callaway & Sant'Anna (2021), "Difference-in-Differences with Multiple Time Periods"

## 23. Interpolation Bias in Control Group Outcomes

**The Weak Link:** The Maddison Project Database 2023 provides near-annual GDP data for GBR, NLD, and FRA, but only sparse benchmark observations for CHN and IND (roughly decadal or less frequent), which are then linearly interpolated to fill the annual panel.

**The Fatal Flaw:** Linear interpolation mechanically smooths the control group's GDP trajectory, artificially reducing its variance and creating a false appearance of stable, parallel pre-trends. This makes the parallel trends assumption appear more plausible than the real (unobserved) annual data would warrant. Furthermore, interpolated data violates the OLS assumption that errors are independent — the interpolation creates deterministic serial correlation in the control group residuals. The DiD estimator may be consistent but the standard errors are unreliable, and the visual parallel trends test is misleading.

**References:**
- Bolt & van Zanden (2024), Maddison Project Database 2023 — documentation notes on data coverage
- Angrist & Pischke (2009), Ch. 8 on measurement error in panel data
