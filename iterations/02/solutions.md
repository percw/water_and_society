# Iteration 02: Solutions

Solutions addressing the limitations identified in [limitations.md](limitations.md).

## 4. The Cliometric Fallacy: Granger Causality on Interpolated GDP Data

**Status:** in-progress

**Approach:** Phase 1R provides statistical safeguards against spurious time-series results:
- **Phase 1R.1 (ADF stationarity tests):** Validates the differencing approach required for Granger causality; tests both levels and first differences with constant and trend specifications.
- **Phase 1R.4 (Permutation test):** Provides a non-parametric alternative that does not depend on the stationarity assumptions violated by interpolated data. If the real series significantly outperforms random permutations, the signal has validity beyond interpolation artifacts.
- **Phase 1R.5 (Benjamini-Hochberg):** Corrects for multiple testing across all Granger tests.

**Remaining gaps:** The interpolated nature of Maddison GDP data is not explicitly flagged or corrected. No alternative econometric approaches (e.g., using only benchmark years, or structural break tests at known data points) have been implemented. The fundamental critique — that lag structure in interpolated data is mathematical artifact — is mitigated but not fully resolved.

---

## 5. NLP Methodological Catastrophe: Synthetic Documents and Pseudo-Co-occurrence

**Status:** in-progress

**Approach:** Phase 2.2 partially addresses this by shifting methodology:
- **PPMI-SVD temporal embeddings** replace Word2Vec for diachronic analysis. This approach uses word frequency profiles within time windows rather than generating synthetic documents, avoiding the pseudo-co-occurrence problem for the embedding analysis.
- Phase 2.2 computes co-occurrence approximations directly from Ngram frequency data rather than fabricating document boundaries.

**Remaining gaps:** Phase 2.1 (LDA topic modeling) still operates on synthetic documents generated from marginal frequencies. The fundamental critique — that LDA requires true document-level co-occurrence — remains valid for the topic modeling results. A real solution would require access to full-text corpora (HathiTrust, ECCO) rather than aggregated Ngram frequencies.

---

## 6. Uncontrolled Polysemy and Dictionary Inflation

**Status:** pending

**Approach:** _To be determined._

No word-sense disambiguation (WSD) has been implemented. The vocabulary lists still include polysemous terms (`power`, `mill`, `engine`) without contextual filtering. A solution would require either: (a) restricting to unambiguous bigrams only, (b) implementing WSD using contextual embeddings, or (c) access to full-text corpora for collocation analysis.

---

## 7. The Endogeneity of Print Culture

**Status:** pending

**Approach:** _To be determined._

No causal identification strategy has been implemented to separate the linguistic signal as cause vs. effect of industrialization. Potential approaches include: instrumental variables, lagged cross-correlation analysis controlling for print volume, or Granger causality with total publication counts as a covariate.
