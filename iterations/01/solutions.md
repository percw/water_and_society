# Iteration 01: Solutions

Solutions addressing the limitations identified in [limitations.md](limitations.md).

## 1. The "Fossil Capital" Critique: Spatial Mobility vs. Temporal Precedence

**Status:** in-progress

**Approach:** Phase 1R robustness validation provides partial mitigation:
- **Phase 1R.4 (Placebo tests):** Tests whether irrelevant vocabularies (religious, weather) also Granger-cause GDP. If they don't, the hydro-linguistic signal has specificity beyond mere temporal coincidence.
- **Phase 1R.4 (Permutation test):** Randomly shuffles the linguistic series and re-tests, providing a non-parametric baseline to confirm the result is not an artifact.
- **Limitations section** explicitly acknowledges that "Granger causality tests temporal precedence, not true causation."

**Remaining gaps:** No formal instrumental-variable or difference-in-differences approach to distinguish spatial mobility (Malm's argument) from temporal precedence. A direct test of the Fossil Capital thesis would require modeling factory relocation data alongside linguistic shifts.

---

## 2. Lexical Conflation and Technological Ambiguity

**Status:** in-progress

**Approach:** Phase 1.5 introduces period-appropriate vocabulary that reduces conflation:
- Separates water infrastructure terms (`water wheel`, `overshot`, `undershot`, `mill race`, `breast wheel`, `water mill`) from fossil-fuel terms (`steam engine`, `coal mine`).
- Uses historically specific bigrams that are less ambiguous than the original unigrams (`pump`, `engine`, `mill`).
- **Phase 1R.3 (Leave-one-out):** Tests whether removing any single word collapses the result, partially controlling for terms that straddle both categories.

**Remaining gaps:** No formal disambiguation of shared terms like "mill" (water mill vs. steam mill) or "engine" (water engine vs. steam engine). Word-sense disambiguation (WSD) on historical text remains unimplemented.

---

## 3. The "Library Bias" and the Secularization of Print Culture

**Status:** in-progress

**Approach:** Acknowledged explicitly in the notebook's Limitations & Future Work section:
- Notes that Google Books Ngram reflects published books, not all societal discourse.
- Future work proposes validation against HathiTrust corpus for cross-corpus consistency.

**Remaining gaps:** No quantitative correction for sampling bias. No comparison to non-book corpora (e.g., newspapers, pamphlets, court records). The Pechenick et al. (2015) critique remains unaddressed at the implementation level.
