# Revision track — *Journal of Global History*

Submitted 9 September 2026. This directory holds everything needed for the referee
round: what has been learned since submission, what would change in a revised
manuscript, and prepared answers to the objections a referee is most likely to raise.

Nothing here has been sent to the journal. The submitted manuscript is
[`submission/01_journal_of_global_history/`](../submission/01_journal_of_global_history/).

---

## Status

| | |
|---|---|
| Manuscript | 12,497 words incl. footnotes; abstract 146 |
| Figures / tables | 5 / 7 |
| Supplementary | `replication_package_anonymous.zip` (29 files, anonymised) |
| Submitted | 9 September 2026, ScholarOne |

---

## What we have learned since submitting

All of this comes from [`src/methods/`](../src/methods/), added 11 September 2026.
It is a Monte Carlo study of the paper's own specification, calibrated to the
British series and reproducing Table 3 exactly.

### 1. The specification is badly oversized

The quadratic-trend + war specification with Newey–West(10) rejects a true null
**17.8%** of the time in the coal equation and **18.6%** in the income equation,
against a nominal 5%. At nominal 1% it rejects 8.5%.

The size-corrected 5% threshold is **p < 0.0029**.

This is a property of HAC standard errors on 131 observations with autocorrelated
residuals, not of the canal dose specifically. It applies to every p-value in
Table 3.

### 2. The headline result survives

Coal under the quadratic trend is p = 0.001, inside the corrected threshold.

The paper's own family-wise bar in §6.2 — "a Bonferroni threshold of about 0.002"
— happens to sit almost exactly on the size-corrected threshold. The paper was
already conservative enough, for a different reason than the real one.

### 3. One sentence is too strong

§4.2: *"With a quadratic trend and a war dummy, coal, iron and services retain
large and significant coefficients."*

Iron is p = 0.013, well outside the corrected threshold. Services at p = 0.002
just survives. **Iron should come out of that list.**

The argument does not rest on it — the next sentence says "Coal is the robust
channel", and §6.2's list of what clears the bar does not include iron.

### 4. The null on income per head is informative but bounded

At the corrected threshold the design has

| Direct effect on income by 1830 | Probability of detecting it |
|---|---|
| 26% | 53% |
| 42% | 82% |
| 59% | 94% |

So the null rules out a *large* rival cause, not a modest one. The paper currently
implies more than this. A revision should state the bound.

### 5. The predetermined dose inherits the same problem

The Priestley authorisation dose has R² = 0.982 on a quadratic trend, against
0.976 for the completion dose. It is **equally trend-like**.

The paper's claim for it is correct as written — §3.5 says only that predetermined
doses "remove contemporaneous feedback" — but a referee may assume it also
strengthens identification. It does not. Worth saying so explicitly.

---

## Prepared responses

**"The canal series comes from Wikipedia."**
Disclosed in §3.2 and §6.3. Corroborated by 152 Priestley authorisations, an 1831
primary source. Validated in §3.2 against the Cambridge Group's dynamic waterways
GIS: our 2,102 miles over 1760–1830 are four-fifths of the documented network
growth, the remainder being post-1830 completions, branches and river work we
exclude. The definitive series would come from CAMPOP's sectional opening dates,
which are not publicly deposited; a request is the obvious next step.

**"Your p-values are too small on trending series."**
Correct, and now quantified — see 1 above. Offer the Monte Carlo as a supplementary
appendix. The headline result survives; the paper's stated Bonferroni bar already
matched the corrected threshold.

**"Income per head shows nothing because you have no power."**
Partly right, and now bounded — see 4. Report the minimum detectable effect.

**"This is British economic history, not global history."**
The reframe of 7 September answers this: the paper opens with Tvedt's comparative
question, §4.6 is a full comparative results section on four cases, and §5.4
restates the thesis as a matching rule. The DiD material is demoted to §4.7.

**"The comparative cases are not tests."**
Agreed, and said so in §6.7 before any referee could. They are labelled readings.

---

## If invited to revise

1. Remove "iron" from §4.2's list.
2. Add one sentence to §6.2 giving the size-corrected threshold.
3. Add the minimum detectable effect to §6.5 or §4.3.
4. Note in §6.1 that the predetermined dose does not fix trend collinearity.
5. Offer the Monte Carlo as an online appendix.
6. Request the CAMPOP sectional dataset and rebuild the mileage series if it arrives.

Items 1–4 cost about sixty words and can be paid for from the existing text.
