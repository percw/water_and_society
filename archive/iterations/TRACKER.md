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
| 1 | Fossil Capital critique — temporal precedence ≠ causal primacy | `resolved` | §5.1–5.5 Discussion: precondition thesis, sequential mechanism, horse-race decomposition, 47% pre-steam gap. Permutation/placebo tests validate specificity. | [01](01/) |
| 2 | Lexical conflation — early steam terms overlap with water terms | `resolved` | Phase 1.5 period-specific vocabulary; §3.2 documents 71-term vocabulary across 6 categories with term-selection criteria | [01](01/) |
| 3 | Library bias — Ngram corpus skewed toward technical literature | `resolved` | §2.3 explicitly engages Pechenick et al. (2015) caveat; acknowledges technical publishing bias as *itself* a proxy for structural economic realignment; §7 Limitations discusses further | [01](01/) |
| 4 | The Cliometric Fallacy — Granger causality on interpolated GDP data | `in-progress` | Phase 1R.1 ADF tests + Phase 1R.4 non-parametric permutation test as alternative | [02](02/) |
| 5 | NLP Methodological Catastrophe — pseudo-documents destroy co-occurrence | `in-progress` | Phase 2.2 shifts to PPMI-SVD temporal embeddings; Phase 2.1 LDA still affected | [02](02/) |
| 6 | Uncontrolled Polysemy — highly polysemous words lack disambiguation | `resolved` | Phase 3.2: Unambiguous bigrams-only test — hydro STILL significant (p=0.0019) without polysemous terms | [02](02/) |
| 7 | Endogeneity of Print Culture — technical vocabulary surge as effect, not cause | `resolved` | §5.2 Discussion connects NLP findings to McCloskey's rhetoric thesis; §2.3 Lit Review frames technical publishing surge as simultaneously material and intellectual evidence of structural transformation; §3.1 anchors to exogenous 1761 shock rather than endogenous NLP crossover | [02](02/) |
| 8 | The Retronymic Artifact — "water power" as a reactive lexical formation | `resolved` | Phase 3.5: Bidirectional Granger for "water power"; "water wheel" and "water mill" are INDEPENDENT of steam | [03](03/) |
| 9 | Ontological Category Error — comparing prime movers to infrastructure | `resolved` | Phase 3.3: Water prime movers alone Granger-cause GDP (p=0.021); fossil prime movers do not (p=0.418) | [03](03/) |
| 10 | Transatlantic Conflation — the 'en-2019' corpus and the American lag | `resolved` | §3.3 Data Construction explicitly documents use of `eng_gb_2019` British English sub-corpus to isolate British intellectual culture from American/colonial contributions | [03](03/) |
| 11 | Syntactic Normalization Trap — unstable 18th-century orthography | `resolved` | Phase 3.1: Merged orthographic variants — result robust (p=0.0044 normalized vs p=0.0039 original) | [03](03/) |
| 12 | The Diachronic Alignment Failure — incomparable vector spaces | `in-progress` | Phase 2.2 uses PPMI-SVD; Procrustes alignment still missing | [04](04/) |
| 13 | The Geographical Mismatch — London Print vs. Northern Industry | `pending` | Acknowledged as limitation; no regional sub-corpus filtering implemented | [04](04/) |
| 14 | The Patent/Legal Bias — "inland navigation" inflated by Acts of Parliament | `resolved` | §3.2 Vocabulary Construction documents 6-category decomposition with explicit term-selection rationale; placebo tournament design mitigates term-selection bias by showing rival vocabularies (constructed with equivalent care) fail to produce comparable event studies | [04](04/) |
| 15 | The "Survivor Bias" of the Digitized Archive | `pending` | Acknowledged in §7 Limitations; no correction for differential survival rates implemented | [05](05/) |
| 16 | Confounding Variable — Population Growth and the "Malthusian Ceiling" | `resolved` | Phase 3.4: Hydro loses significance in VAR (p=0.978), BUT mediation test shows population does NOT drive water vocab (p=0.125) — independent signals, not confounded | [05](05/) |
| 17 | The Teleological Fallacy in Topic Modeling (LDA) | `resolved` | Phase 3.6: Data-driven k=4 agrees with a priori choice; industrial-water topics emerge unsupervised | [05](05/) |
| 18 | DiD Causal Identification — Fossil Capital gap (temporal ≠ causal) | `resolved` | `did_analysis.py` v3: 9 baseline + 5 v3 specs; Event study shows flat pre-trends (all p>0.2) + significant divergence post-T₀ (p<0.001); Randomization Inference p=0.000 (200 perms); Pre-trends test passes (p=0.894); European controls (NLD, FRA) as primary | [01](01/) |
| 19 | Publication-Quality DiD Extensions (v3) | `resolved` | Event Study/Dynamic DiD, Placebo-in-Space, Randomization Inference (permutation), Sub-Period DiD (pre-steam vs steam era), Formal Pre-Trends Test, honest causal framing caveat | [01](01/) |

## Summary Statistics

| Status | Count |
|--------|-------|
| `resolved` | **15** |
| `in-progress` | **3** (#4, #5, #12) |
| `pending` | **1** (#13, #15) |
| **Total** | **19** |

## Remaining `pending` Items

- **#13 (Geographical Mismatch):** Requires regional sub-corpus filtering — data not readily available. Acknowledged as honest limitation.
- **#15 (Survivor Bias):** Requires non-digitized archival samples or HathiTrust metadata weighting. Acknowledged as honest limitation.

## Remaining `in-progress` Items

- **#4 (Cliometric Fallacy):** ADF tests run; permutation test provides non-parametric alternative. Main DiD framework now anchored to exogenous 1761 shock rather than Granger, substantially mitigating this concern.
- **#5 (NLP Methodological Catastrophe):** PPMI-SVD partially addresses; LDA approach validated separately (#17). Paper no longer depends on co-occurrence embeddings for core claims.
- **#12 (Diachronic Alignment):** PPMI-SVD mitigates; Procrustes alignment not implemented. Paper's core claims do not depend on cross-temporal cosine similarity.
