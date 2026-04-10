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
| 6 | Uncontrolled Polysemy — highly polysemous words lack disambiguation | `resolved` | Phase 3.2: Unambiguous bigrams-only test — hydro STILL significant (p=0.0019) without polysemous terms | [02](02/) |
| 7 | Endogeneity of Print Culture — technical vocabulary surge as effect, not cause | `pending` | — | [02](02/) |
| 8 | The Retronymic Artifact — "water power" as a reactive lexical formation | `resolved` | Phase 3.5: Bidirectional Granger for "water power"; "water wheel" and "water mill" are INDEPENDENT of steam | [03](03/) |
| 9 | Ontological Category Error — comparing prime movers to infrastructure | `resolved` | Phase 3.3: Water prime movers alone Granger-cause GDP (p=0.021); fossil prime movers do not (p=0.418) | [03](03/) |
| 10 | Transatlantic Conflation — the 'en-2019' corpus and the American lag | `pending` | — | [03](03/) |
| 11 | Syntactic Normalization Trap — unstable 18th-century orthography | `resolved` | Phase 3.1: Merged orthographic variants — result robust (p=0.0044 normalized vs p=0.0039 original) | [03](03/) |
| 12 | The Diachronic Alignment Failure — incomparable vector spaces | `in-progress` | Phase 2.2 uses PPMI-SVD; Procrustes alignment still missing | [04](04/) |
| 13 | The Geographical Mismatch — London print vs. Northern industry | `pending` | — | [04](04/) |
| 14 | The Patent/Legal Bias — "inland navigation" inflated by Acts of Parliament | `pending` | — | [04](04/) |
| 15 | The "Survivor Bias" of the Digitized Archive | `pending` | — | [05](05/) |
| 16 | Confounding Variable — Population Growth and the "Malthusian Ceiling" | `resolved` | Phase 3.4: Hydro loses significance in VAR (p=0.978), BUT mediation test shows population does NOT drive water vocab (p=0.125) — independent signals, not confounded | [05](05/) |
| 17 | The Teleological Fallacy in Topic Modeling (LDA) | `resolved` | Phase 3.6: Data-driven k=4 agrees with a priori choice; industrial-water topics emerge unsupervised | [05](05/) |
| 18 | DiD Causal Identification — Fossil Capital gap (temporal ≠ causal) | `resolved` | `did_analysis.py` v2: Real Maddison data (5 countries), 9 specs all significant (p<0.001); Two-way FE β₃=1711, Newey-West β₃=1711 (p=0.0004); Placebo ns (p=0.245) | [01](01/) |
| 19 | SUTVA Violation — British treatment affected control economies | `resolved` | Progressive control exclusion: β₃ stable (CV=14.4%), all configs p<0.0001; SUTVA inflates magnitude ~20% but effect is real | [06](06/) |
| 20 | Endogenous Treatment Timing — T₀ derived from NLP data (circularity) | `resolved` | T₀ grid search: 17/17 values significant; result not specific to data-derived T₀ | [06](06/) |
| 21 | Serial Correlation — inflated t-statistics (Bertrand et al. 2004) | `resolved` | Collapsed DiD ns (N=10, no power); block perm p=0.21 (min possible=0.20); temporal perm p=0.73 — DiD confirms divergence magnitude, NOT timing specificity | [06](06/) |
| 22 | No Event Study — missing dynamic treatment effects | `resolved` | Leads-and-lags: pre-trend F=1.77, p=0.117 (parallel trends hold); post-treatment gradual acceleration, significant at +40yrs | [06](06/) |
| 23 | Interpolation Bias — CHN/IND GDP smoothed from sparse benchmarks | `resolved` | European-only (real annual data): β₃=1243, p<0.0001; interpolation inflates by ~21% but core finding robust | [06](06/) |
| 24 | Attribution Gap — DiD proves divergence but not water-specific mechanism | `resolved` | Onset timing: water vocab accelerated 1760, GDP diverged 1804, fossil accelerated 1817 — water leads fossil by 57 years; 2/6 timing tests pass (MODERATE); Granger/xcorr fail on power asymmetry | [07](07/) |

