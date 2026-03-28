# Iteration 03: Solutions

Solutions addressing the limitations identified in [limitations.md](limitations.md).

## 8. The Retronymic Artifact: "Water Power" as a Reactive Lexical Formation

**Status:** pending

**Approach:** _To be determined._

Phase 1.5 introduces "water power" as a key term but does not address the retronym critique. A solution would require analyzing the directionality of lexical emergence — e.g., testing whether "water power" frequency correlates with "steam engine" frequency (reactive formation) or precedes it independently.

---

## 9. Ontological Category Error: Comparing Prime Movers to Infrastructure

**Status:** pending

**Approach:** _To be determined._

The analysis compares infrastructure terms (cotton mill, canal) directly with prime mover terms (steam engine, coal). A solution would require separating vocabulary into ontologically comparable categories and running parallel analyses: infrastructure vs. infrastructure (canal vs. railway) and prime mover vs. prime mover (water wheel vs. steam engine).

---

## 10. Transatlantic Conflation: The 'en-2019' Corpus and the American Lag

**Status:** pending

**Approach:** _To be determined._

The `fetch_data.py` script uses `corpus='en-2019'` which aggregates British and American publications. Google Ngram Viewer offers `eng-gb-2019` (British English) as an alternative. A solution would re-run the entire pipeline with the British-only corpus and compare results.

---

## 11. Syntactic Normalization Trap: Unstable 18th-Century Orthography

**Status:** pending

**Approach:** _To be determined._

No compound-word normalization has been implemented. Terms like "water wheel", "water-wheel", and "waterwheel" are treated as separate n-grams. A solution would merge variant forms by fetching all orthographic variants and summing their frequencies before analysis.
