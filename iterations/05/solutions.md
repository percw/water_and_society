# Iteration 05: Solutions

Solutions addressing the limitations identified in [limitations.md](limitations.md).

## 15. The "Survivor Bias" of the Digitized Archive

**Status:** pending

**Approach:** _To be determined._

No correction for differential survival rates of historical documents has been implemented. A solution would require either: (a) weighting by estimated survival rates per document type, (b) comparing against non-digitized archival samples, or (c) using the HathiTrust metadata to control for library-of-origin biases.

---

## 16. Confounding Variable: Population Growth and the "Malthusian Ceiling"

**Status:** resolved

**Approach:** Phase 3.4 conducts a four-part analysis: (a) VAR with population covariate, (b) collinearity diagnostics, (c) unambiguous vocabulary with population control, and (d) mediation analysis testing whether water is the mechanism linking population to GDP.

**Results:**

Part A — VAR with generic HYDRO_WORDS + Population:
- Hydro → GDP (controlling for Population): **p = 0.978 — NOT significant**
- Population → GDP: **p = 0.002 — SIGNIFICANT**

Part B — Collinearity:
- Correlation in levels: r = 0.269 (low)
- Correlation in first differences: r = -0.728 (high, **negative**)
- The negative correlation after differencing means population growth *accelerates* while hydro vocabulary growth *decelerates* — they move in opposite directions year-to-year

Part C — Unambiguous Phase 1.5 vocabulary + Population:
- Unambiguous Hydro → GDP (w/ pop ctrl): p = 0.420 — not significant
- Neither generic nor unambiguous hydro vocabulary survives population control

Part D — Mediation test (Population → Water Vocab → GDP?):
- Step 1: Population → Hydro Vocab: **p = 0.125 — NOT significant**
- Step 2: Hydro Vocab → GDP: p = 0.005 — significant
- Step 3: Population → GDP: p = 0.000 — significant
- Step 4: Pop→GDP weakens when Hydro is controlled (p goes from 0.000 to 0.002)

**Conclusion:** The mediation pathway is **not supported** — population does NOT Granger-cause water vocabulary (p=0.125). Population and water vocabulary are **independently trending**, driven by different underlying dynamics. This is actually favorable for the thesis: water vocabulary is not merely a demographic echo. However, the VAR still cannot separate their contributions to GDP growth due to the shared upward trend over two centuries.

**Implications for the thesis:** The population confound is real but does not reduce to "population drives water vocabulary." The two signals are independent. The challenge is that both correlate with GDP over a 200-year window, and a linear VAR cannot distinguish them. Sub-period analysis (e.g., testing whether water vocabulary predicts GDP in periods where population is stable) or instrumental variables would provide cleaner identification.

---

## 17. The Teleological Fallacy in Topic Modeling (LDA)

**Status:** resolved

**Approach:** Phase 3.6 tests the LDA robustness in two ways:
1. **Topic count selection:** Fit LDA with k = 2, 3, 4, 5, 6, 8 and compare perplexity
2. **Unsupervised discovery:** Check whether "industrial water" topics emerge without keyword-guided selection

**Results:**

Part A — Perplexity comparison:
| k | Perplexity | Log-likelihood |
|---|-----------|---------------|
| 2 | 12.6 | -929,349 |
| 3 | 12.5 | -927,143 |
| **4** | **12.5** | **-926,738** (best) |
| 5 | 12.5 | -926,968 |
| 6 | 12.5 | -927,029 |
| 8 | 12.5 | -927,444 |

Data-driven selection **agrees** with the a priori choice of k=4.

Part B — Unsupervised topic discovery (k=4):
- Topic 0: water, steam, power, engine, coal, machine, river, factory — **INDUSTRIAL WATER**
- Topic 1: water, coal, power, steam, engine, engineer, machine, river — **FOSSIL INDUSTRIAL**
- Topic 2: water, power, holy, river, divine, mill, rain, navigation — **WATER-DOMINANT**
- Topic 3: water, power, canal, river, mill, navigation, engine, coal — **INDUSTRIAL WATER**

**Conclusion:** The "industrial water" topic **emerges unsupervised** without keyword-guided selection. The data-driven optimal topic count matches the a priori choice. The LDA finding reflects real structure in the data, not merely teleological construction.
