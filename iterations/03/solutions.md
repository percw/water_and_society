# Iteration 03: Solutions

Solutions addressing the limitations identified in [limitations.md](limitations.md).

## 8. The Retronymic Artifact: "Water Power" as a Reactive Lexical Formation

**Status:** resolved

**Approach:** Phase 3.5 tests whether water technology terms are retronyms (reactive to steam) or independent precursors, using bidirectional Granger causality between each term and `steam`.

**Results:**
| Term | Steam→Term p | Term→Steam p | Verdict |
|------|-------------|-------------|---------|
| water power | 0.039 | 0.0005 | BIDIRECTIONAL |
| water wheel | 0.065 | 0.0015 | INDEPENDENT |
| water mill | 0.085 | 0.0041 | INDEPENDENT |
| water engine | 0.551 | 0.166 | NO RELATION |

**Conclusion:** "Water power" shows bidirectional feedback with steam (partially retronymic), but "water wheel" and "water mill" are **independent** — they Granger-cause steam but steam does NOT Granger-cause them. The core water technology terms precede steam independently, supporting the first-mover thesis. However, "water power" as a general term should be interpreted with caution as it is partially reactive.

---

## 9. Ontological Category Error: Comparing Prime Movers to Infrastructure

**Status:** resolved

**Approach:** Phase 3.3 separates the vocabulary into ontologically comparable categories and runs Granger causality independently for each:
- **Prime Movers** (energy conversion): water wheel, overshot, undershot, breast wheel, mill wheel, water power, turbine vs. steam, coal
- **Infrastructure** (transport/built): inland navigation, canal navigation, navigable, barge, towpath, waterway, sluice, penstock, mill race
- **Manufacturing Sites**: cotton mill, spinning mill, corn mill, fulling mill, water mill, water frame

**Results:**
| Category | p-value | Lag | Significant? |
|----------|---------|-----|-------------|
| Water Prime Movers | 0.021 | 1 | Yes |
| Fossil Prime Movers | 0.418 | 4 | No |
| Water Infrastructure | 0.039 | 1 | Yes |
| Water Manufacturing | 0.002 | 1 | Yes |

**Conclusion:** Water **prime movers alone** Granger-cause GDP (p=0.021) while fossil prime movers do not (p=0.418). The finding holds even in the strictest like-for-like comparison. The ontological category critique does NOT invalidate the core finding.

---

## 10. Transatlantic Conflation: The 'en-2019' Corpus and the American Lag

**Status:** pending

**Approach:** _To be determined._

The `fetch_data.py` script uses `corpus='en-2019'` which aggregates British and American publications. Google Ngram Viewer offers `eng-gb-2019` (British English) as an alternative. A solution would re-run the entire pipeline with the British-only corpus and compare results.

---

## 11. Syntactic Normalization Trap: Unstable 18th-Century Orthography

**Status:** resolved

**Approach:** Phase 3.1 merges orthographic variants of compound words and re-runs Granger causality to test whether results depend on spelling conventions.

Merged: `water wheel` + `waterwheel` → combined form (peak increases from 1.5e-05 to 1.8e-05).

**Results:**
| Version | p-value | Lag | Significant? |
|---------|---------|-----|-------------|
| Original (un-normalized) | 0.0039 | 1 | Yes |
| Normalized (merged variants) | 0.0044 | 1 | Yes |

**Conclusion:** The result is **robust to orthographic normalization**. Merging variant forms barely changes the p-value (0.0039 → 0.0044). The finding does not depend on selective spelling conventions.
