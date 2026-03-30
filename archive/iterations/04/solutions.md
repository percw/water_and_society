# Iteration 04: Solutions

Solutions addressing the limitations identified in [limitations.md](limitations.md).

## 12. The Diachronic Alignment Failure: Incomparable Vector Spaces

**Status:** in-progress

**Approach:** Phase 2.2 partially addresses this by using PPMI-SVD instead of independent Word2Vec models:
- PPMI-SVD computes embeddings from co-occurrence matrices derived from frequency profiles, allowing comparison across time periods using the same dimensional basis.
- Cosine similarity is computed within a shared frequency-derived space rather than across independently trained embedding models.

**Remaining gaps:** No formal Orthogonal Procrustes alignment or canonical correlation analysis has been implemented. If separate embedding spaces per decade are used, they must be mathematically aligned to a common coordinate system before comparison. The current approach mitigates but does not fully resolve the alignment problem.

---

## 13. The Geographical Mismatch: London Print vs. Northern Industry

**Status:** pending

**Approach:** _To be determined._

No geographic filtering of the corpus has been implemented. A solution would require either: (a) using regionally tagged sub-corpora if available, (b) filtering by publisher location metadata, or (c) supplementing with Northern archival sources (e.g., Manchester Literary and Philosophical Society proceedings).

---

## 14. The Patent/Legal Bias in Infrastructure Terminology

**Status:** pending

**Approach:** _To be determined._

Phase 1.5 includes "inland navigation" and "canal navigation" as key terms without filtering for legal/legislative vs. operational documents. A solution would require either: (a) removing legislative terms from the vocabulary, (b) controlling for Acts of Parliament publication volume, or (c) comparing legislative vs. non-legislative sub-corpora.
