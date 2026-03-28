# Iteration 05: Solutions

Solutions addressing the limitations identified in [limitations.md](limitations.md).

## 15. The "Survivor Bias" of the Digitized Archive

**Status:** pending

**Approach:** _To be determined._

No correction for differential survival rates of historical documents has been implemented. A solution would require either: (a) weighting by estimated survival rates per document type, (b) comparing against non-digitized archival samples, or (c) using the HathiTrust metadata to control for library-of-origin biases.

---

## 16. Confounding Variable: Population Growth and the "Malthusian Ceiling"

**Status:** resolved

**Approach:** Phase 3.4 adds British historical population data (Wrigley & Schofield 1981; Mitchell 1988) as a covariate in a VAR model, testing whether the hydro-linguistic signal retains predictive power after controlling for demographic pressure.

**Results:**
- VAR model: GDP ~ Hydro + Population (first-differenced, AIC-selected lag = 1)
- **Hydro → GDP (controlling for Population): p = 0.978 — NOT significant**
- **Population → GDP: p = 0.002 — SIGNIFICANT**
- Comparison: Hydro → GDP (bivariate, no population control): p = 0.005 — significant

**Conclusion:** This is a **critical finding that challenges the core hypothesis**. When population growth is included as a covariate, the hydro-linguistic signal completely loses its predictive power (p drops from 0.005 to 0.978). Population growth is the dominant Granger-causal predictor of GDP. This strongly suggests that the linguistic rise of water vocabulary reflects demographic pressure driving agricultural/infrastructure expansion, NOT an independent "first mover" technological revolution. The original bivariate Granger result was confounded by the omitted population variable.

**Implications for the thesis:** The Tvedt hypothesis is not necessarily wrong — water infrastructure was genuinely important — but the linguistic signal cannot be cleanly separated from the demographic signal using this methodology. Future work should test whether the relationship holds within sub-periods (pre/post 1800) or with different vocabulary subsets.

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
