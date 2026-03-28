# Iterations Tracker

Master log for tracking limitations and their resolution across iterations.

**Workflow:** Find limitations → log in `XX/limitations.md` → pick one → mark `in-progress` → implement solution → document in `XX/solutions.md` → mark `resolved`

## Status Legend

| Status | Meaning |
|--------|---------|
| `pending` | Identified, not yet addressed |
| `in-progress` | Actively being worked on |
| `resolved` | Solution implemented and documented |
| `revisited` | Previously resolved, reopened due to new findings |

## Tracker

| # | Limitation | Status | Solution Summary | Iteration |
|---|-----------|--------|-----------------|-----------|
| 1 | Fossil Capital critique — temporal precedence ≠ causal primacy | `in-progress` | Phase 1R permutation/placebo tests validate specificity; acknowledged in Limitations section | [01](01/) |
| 2 | Lexical conflation — early steam terms overlap with water terms | `in-progress` | Phase 1.5 introduces period-specific vocabulary to reduce overlap | [01](01/) |
| 3 | Library bias — Ngram corpus skewed toward technical literature | `in-progress` | Acknowledged in Limitations section; future work proposes HathiTrust validation | [01](01/) |
| 4 | The Cliometric Fallacy — Granger causality on interpolated GDP data | `in-progress` | Phase 1R.1 ADF tests + Phase 1R.4 non-parametric permutation test as alternative | [02](02/) |
| 5 | NLP Methodological Catastrophe — pseudo-documents destroy co-occurrence | `in-progress` | Phase 2.2 shifts to PPMI-SVD temporal embeddings; Phase 2.1 LDA still affected | [02](02/) |
| 6 | Uncontrolled Polysemy — highly polysemous words lack disambiguation | `pending` | — | [02](02/) |
| 7 | Endogeneity of Print Culture — technical vocabulary surge as effect, not cause | `pending` | — | [02](02/) |
| 8 | The Retronymic Artifact — "water power" as a reactive lexical formation | `pending` | — | [03](03/) |
| 9 | Ontological Category Error — comparing prime movers to infrastructure | `pending` | — | [03](03/) |
| 10 | Transatlantic Conflation — the 'en-2019' corpus and the American lag | `pending` | — | [03](03/) |
| 11 | Syntactic Normalization Trap — unstable 18th-century orthography | `pending` | — | [03](03/) |
| 12 | The Diachronic Alignment Failure — incomparable vector spaces | `in-progress` | Phase 2.2 uses PPMI-SVD; Procrustes alignment still missing | [04](04/) |
| 13 | The Geographical Mismatch — London print vs. Northern industry | `pending` | — | [04](04/) |
| 14 | The Patent/Legal Bias — "inland navigation" inflated by Acts of Parliament | `pending` | — | [04](04/) |
| 15 | The "Survivor Bias" of the Digitized Archive | `pending` | — | [05](05/) |
| 16 | Confounding Variable — Population Growth and the "Malthusian Ceiling" | `pending` | — | [05](05/) |
| 17 | The Teleological Fallacy in Topic Modeling (LDA) | `pending` | — | [05](05/) |
