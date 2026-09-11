# Expansion track — when can an accumulating dose identify a sequence?

A methods project growing out of the canals paper. It is not a second history
paper; it asks whether the design that paper uses can bear the weight put on it,
and under what conditions.

Code lives in [`src/methods/`](../src/methods/). Nothing here is submitted anywhere.

---

## The question

A large class of claims in historical social science has the form *X was a
precondition for Y*, where X is a smooth accumulating stock: canal miles,
railway miles, sewer miles, schooling, financial depth, transmission capacity.
Such claims are usually argued narratively. When they are tested, they are tested
with regressions on trending series, and the field has no guidance on when that
can work.

The canals paper infers a precondition from a pattern: **the dose predicts the
intermediate and not the final outcome.** That inference is valid only if the
specification (i) rejects at the rate it claims and (ii) could have detected a
direct effect had one been there. Neither is obvious when the dose is 97.6% a
quadratic trend.

## What exists

| File | What it does |
|---|---|
| [`dose_identification.py`](../src/methods/dose_identification.py) | Reusable framework: `Design.size()` and `Design.power()` for any dose, sample size and noise calibration |
| [`identification_simulation.py`](../src/methods/identification_simulation.py) | Application 1: the British canal dose. Figure 6 |
| [`run_boundary.py`](../src/methods/run_boundary.py) | The boundary sweep across dose shapes. Figure 7, `data/external/boundary_sweep.csv` |

## Findings so far

**The two problems are separate, and only one is about the dose.**

*Size distortion is a constant.* Across dose shapes spanning R² = 0.86 to 0.995
on a quadratic trend, the nominal 5% test rejects between 14% and 21% of the time,
with no trend in that relationship. It is a property of Newey–West errors on ~130
observations with autocorrelated residuals. The fix is a corrected threshold of
roughly **p < 0.003**, and it applies whatever the dose looks like.

*Power collapses with trendiness.* The smallest effect detectable with 80% power
rises steeply as the dose approaches a pure trend:

| Dose R² on a quadratic trend | Smallest detectable effect |
|---|---|
| 0.86–0.90 | ~13% |
| 0.93–0.94 | ~16–23% |
| 0.95–0.96 | ~23–31% |
| **0.976 (British canals)** | **~42%** |
| 0.98–0.99 | ~46–65% |
| 0.995 | ~100% |

Above about R² = 0.99 a null result carries no information at all: nothing short
of a doubling would have been visible.

**Both real British doses sit in the difficult region.** Canal miles are at 0.976,
the Priestley authorisations at 0.982. The predetermined dose removes
contemporaneous feedback, as the paper claims, but inherits the same blindness.

## The transportable diagnostic

Before running a dose-response regression on an accumulating stock:

1. Regress the dose on a quadratic trend and read the R².
2. Above 0.95, treat nominal p-values as meaningless; demand p < 0.003.
3. Above 0.99, do not report a null as evidence of absence.

That is three lines of code and it is currently nobody's habit.

## Next steps

1. **A second application with a less trend-like dose.** Transmission-grid buildout
   is the natural candidate: capacity arrives in discrete, dated, policy-driven
   episodes, so the dose should sit nearer R² = 0.90 where the design has teeth.
   Annual data by country from ENTSO-E, IEA and Ember. Requires data acquisition,
   which has not been done.
2. **Vary n.** Everything here is at n = 131. The size distortion is a small-sample
   HAC problem and should shrink; how fast is an open question.
3. **Alternatives to HAC.** A wild bootstrap or a fixed-b correction may restore
   size without the Monte Carlo. Worth checking before recommending a threshold.
4. **Formalise.** Write the DAG and the exclusion restriction that distinguish
   a precondition from a rival cause. This is the part that would make it a method
   rather than a diagnostic.

## Honest scope

This is not a new method on the level of NCA or QCA. Every estimator used is off
the shelf. What it produces is a boundary condition with numbers attached, and a
diagnostic anyone can apply to their own dose in three lines.

That is a narrow, defensible contribution and it is the right size of claim. The
method would be established by a second application, not by asserting novelty.
