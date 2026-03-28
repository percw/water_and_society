# Iteration 05: Solutions

Solutions addressing the limitations identified in [limitations.md](limitations.md).

## 15. The "Survivor Bias" of the Digitized Archive

**Status:** pending

**Approach:** _To be determined._

No correction for differential survival rates of historical documents has been implemented. A solution would require either: (a) weighting by estimated survival rates per document type, (b) comparing against non-digitized archival samples, or (c) using the HathiTrust metadata to control for library-of-origin biases.

---

## 16. Confounding Variable: Population Growth and the "Malthusian Ceiling"

**Status:** pending

**Approach:** _To be determined._

No population data has been incorporated into the models. A solution would add historical population estimates as a covariate in the Granger causality tests, or run a multivariate VAR model including population growth, linguistic frequency, and GDP per capita to control for the demographic confound.

---

## 17. The Teleological Fallacy in Topic Modeling (LDA)

**Status:** pending

**Approach:** _To be determined._

Phase 2.1 uses prespecified vocabulary to identify "industrial water" topics. A solution would require: (a) running unsupervised LDA without keyword-guided topic selection, (b) testing multiple topic numbers (k) with held-out perplexity validation, or (c) using a non-parametric topic model (e.g., HDP) that discovers the number of topics from the data.
