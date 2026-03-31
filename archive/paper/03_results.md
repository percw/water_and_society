# 3. Results

The linguistic analysis reveals a structured temporal relationship between the cultural integration of water technology and Britain's economic performance, suggesting that early industrial divergence was closely associated with hydro-infrastructure development rather than fossil fuels.

### 3.1 Summary Statistics
Table 1 provides descriptive statistics for the core analytical panel (1700–1900), encompassing annual GDP per capita observations for Great Britain (treatment) and the continental controls (France and the Netherlands).

**Table 1: Summary Statistics (1700–1900)**

| Variable | Obs | Mean | Std. Dev. | Min | Max |
|:---|---:|---:|---:|---:|---:|
| GDP per Capita (1990 GK$) | 603 | 1950.4 | 845.2 | 890.0 | 4520.0 |
| Log GDP per Capita | 603 | 7.48 | 0.42 | 6.79 | 8.41 |
| Treated (GBR=1) | 603 | 0.33 | 0.47 | 0.00 | 1.00 |
| Post (Year $\ge$ 1766) | 603 | 0.67 | 0.47 | 0.00 | 1.00 |
| DiD Interaction | 603 | 0.22 | 0.42 | 0.00 | 1.00 |

### 3.2 The 1766 Linguistic Crossover
Trajectory analysis of the `eng_gb_2019` vocabulary corpus indicates a distinct structural shift occurring toward the latter half of the 18th century. Analysis of 71 key technological and social terms reveals that in the year **1766**, the frequency of "commodified water" terminology crossed and overtook naturalistic or hazard-based uses of water terminology.

This structural shift in the British lexicon represents the identification marker of when water transitioned culturally from an uncontrollable natural force into a harnessed, engineered asset. This structural break is plotted in **Figure 1** relative to the concurrent takeoff of British GDP per capita.

<div align="center">
  <img src="../../data/did_figure_one.png" alt="Figure 1: Identification of the British Hydro-Social Shift" width="800">
  <br>
  <em><strong>Figure 1: Identification of the British Hydro-Social Shift.</strong> The data plots the normalized rolling frequencies of technical hydro-infrastructure vocabulary against fossil/steam terminology. The crossover occurs at $T_0=1766$. This structural break in the British lexicon aligns with the initial takeoff of the GDP per capita gap against continental controls (France and the Netherlands). The approximately 50-year gap between the hydro-social shift and the eventual steam transition (post-1810) is consistent with the temporal precedence of water infrastructure over mineral extraction.</em>
</div>

### 3.3 Difference-in-Differences (DiD) Estimation
Using the 1766 linguistic crossover as the $T_0$ treatment intervention, we executed a DiD regression on annual Maddison Project GDP per capita estimates (Bolt and van Zanden 2020). Assigning Britain as the treatment group against continental European controls (France and the Netherlands), we specify Newey-West HAC standard errors (lag=3) to address serial autocorrelation in multi-century panel data.

The resulting interaction coefficient ($\beta_3$) is **1,292.01** ($p < 0.001$), indicating that Britain's GDP per capita diverged by an additional ~$1,292 relative to continental controls following the hydro-social shift. The formal regression parameters are presented in **Table 2**.

**Table 2: DiD Regression Output (T0 = 1766, Controls: NLD, FRA)**

| Variable | Coefficient | Std. Error | t-statistic | P>\|t\| | [0.025 | 0.975] |
|:---|---:|---:|---:|---:|---:|---:|
| Intercept | 2835.8373 | 95.777 | 29.609 | 0.000 | 2647.738 | 3023.936 |
| Treated (GBR) | -242.3070 | 165.890 | -1.461 | 0.145 | -568.104 | 83.490 |
| Post (>=1766) | 419.6301 | 116.867 | 3.591 | 0.000 | 190.112 | 649.148 |
| **DiD_Interaction** | **1292.0174** | **202.419** | **6.383** | **0.000** | **894.480** | **1689.555** |

*(Note: N=603, R-squared: 0.214, F-Statistic: 54.48. Dependent variable is Historical GDP per capita in 1990 international Geary-Khamis dollars. The two-way fixed effects specification yields R-squared: 0.884 with a consistent DiD coefficient of 1,612.6; see robustness discussion in Section 2.4.)*

### 3.4 Event Study & Parallel Trends
The dynamic DiD event study validates the parallel trends assumption (**Figure 2**). Pre-treatment bins spanning 60 years prior to 1766 yield coefficients statistically indistinguishable from zero, addressing concerns of pre-existing trajectory bias. Following 1766, coefficients rise sharply and consistently, indicating a systemic economic acceleration spanning the established canal era (1760–1830).

<div align="center">
  <img src="../../data/did_event_study.png" alt="Figure 2: Dynamic DiD Event Study" width="800">
  <br>
  <em><strong>Figure 2: Dynamic DiD Event Study.</strong> 5-year binned event study relative to the 1766 hydro-social treatment ($T_0=0$). The flat pre-treatment coefficients spanning 60 years prior to the break support the parallel trends assumption. Following the break, the coefficient rises sharply and steadily, with the treatment window aligning specifically with the era of mass canal engineering rather than late-stage fossil industrialization.</em>
</div>

### 3.5 Robustness Checks
To ensure the observed effect was not an artifact of a generalized 18th-century European aggregate takeoff or a spurious correlation, the model was subjected to "Placebo-in-Space" and "Placebo-in-Time" falsification tournaments.

**Vocabulary Falsification:** When substituting the hydro-social treatment dates with alternative industrial inflection points (e.g., extracting the crossover parameters for *coal*, *textile*, or *financial* vocabulary clusters), the statistical validity of the event study collapsed (**Figure 3**). Only the water hypothesis produced a clean, non-noisy event study with valid pre-trends.

<div align="center">
  <img src="../../data/did_vocab_tournament.png" alt="Figure 3: Placebo Vocabulary Tournament" width="800">
  <br>
  <em><strong>Figure 3: Placebo Vocabulary Tournament.</strong> Falsification test executing event studies against the structural break dates of rival textual corpora. Only the hydro-social treatment (Panel a) yields a statistically clean distribution matching economic takeoff. Rival inflection points derived from coal (b), textiles (c), and finance (d) display high volatility and statistically invalid pre-trends, supporting the specificity of water infrastructure over generalized 18th-century development.</em>
</div>

**Control Falsification:** Assigning the 1766 treatment synthetically to the Netherlands ($p = 0.154$), China ($p = 0.008$), and India ($p = 0.107$) yielded non-significant or negatively significant findings, indicating that the takeoff effect was specific to Great Britain.

**The Pre-Steam Contribution:** Comparing Britain's GDP per capita lead over the mean of France and the Netherlands at three temporal benchmarks yields the following decomposition: in 1700 (baseline), Britain trailed by approximately $-155$ international dollars; by 1810 (the end of the canal era), Britain led by approximately $+1,150$; and by 1900 (peak steam), the lead had grown to approximately $+2,649$. The pre-steam contribution—measured as the share of the 1700-to-1900 GDP gap established by 1810—is thus approximately $(1150 - (-155)) / (2649 - (-155)) \approx 47\%$. This calculation is a descriptive accounting exercise rather than a causal estimate, but it illustrates the quantitative significance of the pre-steam era: nearly half of Britain's ultimate industrial lead was established during the height of the canal and water wheel era, decades before steam power reached critical mass to influence national labor productivity.
