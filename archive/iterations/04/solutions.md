# Iteration 04: Solutions

Solutions addressing the limitations identified in [limitations.md](limitations.md).

## 12. The Diachronic Alignment Failure: Incomparable Vector Spaces

**Status:** in-progress

**Approach:** Phase 2.2 partially addresses this by using PPMI-SVD instead of independent Word2Vec models:
- PPMI-SVD computes embeddings from co-occurrence matrices derived from frequency profiles, allowing comparison across time periods using the same dimensional basis.
- Cosine similarity is computed within a shared frequency-derived space rather than across independently trained embedding models.

**Remaining gaps:** No formal Orthogonal Procrustes alignment or canonical correlation analysis has been implemented. If separate embedding spaces per decade are used, they must be mathematically aligned to a common coordinate system before comparison. The current approach mitigates but does not fully resolve the alignment problem.

**Note (2026-04-07):** The paper's core claims no longer depend on cross-temporal cosine similarity. The primary identification strategy uses (a) composite frequency indices with Savitzky-Golay smoothing and (b) a formal DiD framework anchored to the exogenous 1761 Bridgewater Canal shock. The diachronic embedding analysis is supplementary.

---

## 13. The Geographical Mismatch: London Print vs. Northern Industry

**Status:** pending

**Approach:** _Acknowledged as honest limitation in the manuscript._

No geographic filtering of the corpus has been implemented. A solution would require either: (a) using regionally tagged sub-corpora if available, (b) filtering by publisher location metadata, or (c) supplementing with Northern archival sources (e.g., Manchester Literary and Philosophical Society proceedings).

**Note (2026-04-07):** This limitation is acknowledged transparently in §7 (Limitations). However, the concern is partially mitigated by the fact that parliamentary acts, engineering treatises, and London-based technical publications are themselves evidence of *national-level institutional attention* to water infrastructure — which is what the paper's "epistemological shift" argument (§5.2) actually measures.

---

## 14. The Patent/Legal Bias in Infrastructure Terminology

**Status:** resolved

**Approach:** §3.2 (Vocabulary Construction) now documents the full 71-term vocabulary organized into 6 analytically distinct categories with explicit term-selection criteria. The key mitigation strategies are:

1. **Category separation:** Legislative/bureaucratic terms ("inland navigation", "canal navigation") are classified separately from mechanical terms ("water wheel", "overshot", "mill race"), allowing readers to assess which categories drive the results.

2. **Placebo tournament design:** The falsification tournament constructs rival vocabularies (coal mining, textile, financial, agricultural, steam/mechanical) with *equivalent care*, subjecting each to identical DiD event study analysis. If the hydro signal were merely a bureaucratic artifact, we would expect the financial or legislative placebos to produce comparable event study patterns — they do not.

3. **Term-selection criteria:** §3.2 documents three explicit selection criteria: (a) documented usage in 18th-century primary sources, (b) sufficient frequency in the Ngram corpus for stable annual estimates, and (c) analytical distinctiveness within categories.

**Result:** The legislative bias concern is acknowledged but empirically contained by the placebo design. The water infrastructure shock remains the only vocabulary category producing a clean event study with flat pre-trends and monotonically increasing post-treatment effects.
