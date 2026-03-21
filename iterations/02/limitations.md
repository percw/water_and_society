# Iteration 02: Limitations Emerging from Iteration 01 Solutions

**Date:** 2026-03-21

The solutions in iteration 01 strengthened the thesis against three external critiques but introduced new internal weaknesses. This log documents what is still wrong — problems generated *by* the solutions themselves, not carried over from before.

## 4. Toda-Yamamoto Failure: The Levels Problem

**The Weak Link:** The Toda-Yamamoto augmented Granger test returned p = 0.79 — complete non-significance.

**Why This Matters:** Standard Granger causality operates on first-differenced (stationary) data. Differencing strips out the long-run trend and tests only whether *short-run changes* in hydro vocabulary predict *short-run changes* in GDP. The TY test is specifically designed to test causality in *levels* — does the *cumulative stock* of hydro-industrial language predict the *level* of GDP?

Its failure means the causal claim holds only for year-to-year fluctuations, not for the sustained multi-decade trajectory that is the core historical argument. A reviewer can argue: "Your finding says annual wiggles in water vocabulary predict annual wiggles in GDP. It says nothing about whether the broad rise of hydraulic culture drove the broad rise of industrial output — which is the actual thesis."

**Severity:** High. The thesis is a long-run historical argument tested with a short-run statistical method.

## 5. Impulse Response Sign Inversion

**The Weak Link:** The impulse response function (IRF) from the VAR model showed a *negative* cumulative GDP response to a positive hydro-language shock.

**Why This Matters:** If water vocabulary genuinely drives GDP growth, a positive shock to hydro-language should produce a positive GDP response. The negative sign means the VAR — the same model framework used for the Granger tests — tells a contradictory story when asked to trace the *mechanism* rather than just the *predictive direction*. The Granger test says "hydro predicts GDP." The IRF says "but the prediction is: GDP goes *down*."

This was flagged as "Cholesky ordering sensitive," which is true — IRFs depend on which variable is ordered first. But this is not a dismissal. A reviewer will say: "If the result flips based on an arbitrary ordering choice, the structural relationship is not identified."

**Severity:** High. The causal mechanism implied by the VAR contradicts the thesis.

## 6. Pechenick Ratio Non-Significance

**The Weak Link:** The Pechenick-normalized hydro ratio (hydro share of total technical vocabulary) does not predict GDP (p = 0.61).

**Why This Matters:** The OLS detrending solution showed that the hydro *residual* predicts GDP after removing the common technical trend. But the ratio test showed that water's *relative prominence* within technical literature does not matter — only its *absolute frequency* does. This opens a specific line of attack:

The absolute frequency of hydro terms rises because *all* technical terms rise (more technical books published). The OLS residual captures whatever is left after removing the *linear* component of that rise. But library composition bias may not be linear — if technical publishing accelerated nonlinearly (exponential growth of journals, encyclopedias, patent literature), then a linear OLS detrend under-corrects, and the residual still contains library artifact.

In short: the ratio says "water's share doesn't matter," and the OLS says "something about water's level still matters after linear correction." These are not contradictory, but the gap between them is exactly where a nonlinear corpus artifact could hide.

**Severity:** Medium. The detrending method may be insufficient for the bias it claims to correct.

## 7. Small-N Fragility and Multiple Comparisons

**The Weak Link:** All tests operate on approximately 20 observations (annual GDP, 1700-1900, interpolated or averaged into ~20 data points for Granger lag testing). The study runs at least 8 distinct hypothesis tests (forward Granger, reverse Granger, TY, pure hydro, pure fossil, detrended hydro, detrended fossil, Pechenick ratio).

**Why This Matters:**

1. **Small N**: With ~20 effective observations and 2-4 lag terms consumed, the degrees of freedom are thin. P-values from F-tests with 15-18 residual degrees of freedom are not robust — small perturbations in the data (dropping one year, shifting the interpolation window) can move results across the significance threshold.

2. **Multiple comparisons**: Eight tests at alpha = 0.05 gives an expected ~0.4 false positives by chance alone. No correction (Bonferroni, Holm, FDR) has been applied. The headline result of p = 0.003 survives Bonferroni correction (adjusted threshold = 0.006), but the detrended result (p = 0.019) does not (adjusted threshold = 0.006). The library bias solution is the weakest link after correction.

**Severity:** Medium. The core disambiguation result (p = 0.003) survives, but the detrending result (p = 0.019) becomes marginal-to-non-significant after multiple comparison correction.

## Summary Table

| # | Limitation | Severity | Source |
|---|-----------|----------|--------|
| 4 | TY failure — causal claim holds only in differences, not levels | High | Solution 1 |
| 5 | IRF sign inversion — VAR mechanism contradicts thesis | High | Solution 1 |
| 6 | Pechenick ratio non-significance — linear detrend may under-correct | Medium | Solution 3 |
| 7 | Small-N fragility + no multiple comparison correction | Medium | All solutions |
