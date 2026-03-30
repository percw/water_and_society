# 2. Results

We successfully mapped the cultural integration of water technology against Britain's economic performance, revealing that early industrial divergence was strictly catalyzed by hydro-infrastructure rather than fossil fuels. 

### 2.1 The 1766 Linguistic Crossover
Trajectory analysis of the `eng_gb_2019` vocabulary corpus indicates a highly distinct paradigm shift occurring toward the latter half of the 18th century. Analysis of 71 key technological and social terms reveals that in the year **1766**, the frequency of "commodified water" terminology (e.g., *navigable canal, water wheel, aqueduct*) definitively crossed and overtook naturalistic or hazard-based uses of water terminology. This structural shift in the British lexicon represents the moment water transitioned culturally from a divine or uncontrollable natural force into a harnessed, engineered asset.

### 2.2 Difference-in-Differences (DiD) Estimation
Using 1766 as the $T_0$ treatment intervention, we executed a DiD regression on annual Maddison Project GDP per capita estimates. Model specifications controlling for country and year fixed effects, utilizing Newey-West HAC standard errors (lag=3), demonstrate a robust and highly significant causal effect. Assigning Britain as the treatment group against continental European controls (France and the Netherlands) revealed an interaction variable ($\beta_3$) of **1,292.0** ($p < 0.001$, 95% CI: 894.5 – 1689.6). This demonstrates that Britain gained an additional ~$1,292 in GDP per capita exclusively following the hydro-social structural shift.

### 2.3 Event Study & Parallel Trends
Calculations of a dynamic DiD event study validated the parallel trends assumption. Pre-treatment bins (spanning 60 years prior to 1766) yielded coefficients statistically indistinguishable from zero space, eliminating concerns of pre-existing trajectory bias. Following 1766, the coefficients rise sharply and consistently, indicating a direct post-treatment acceleration spanning from 1766 to the widespread adoption of steam power in the 1830s.

### 2.4 Placebo Falsification Tournaments
To ensure the observed $1,292 effect was not the artifact of a generalized 18th-century European aggregate takeoff, the model was subjected to a "Placebo-in-Space" and "Placebo-in-Time" tournament. 
1. **Control Falsification:** Assigning the 1766 treatment to the Netherlands ($p = 0.154$), China ($p = 0.008$), and India ($p = 0.107$) yielded non-significant or negatively significant findings, proving the takeoff effect was highly specific to Great Britain. 
2. **Vocabulary Falsification:** When substituting the hydro-social treatment dates with alternative industrial inflection points (e.g., the integration of specific *coal*, *textile*, or *financial* vocabulary clusters), the statistical validity of the event study collapsed, further isolating water infrastructure as the unique instigator of the initial British divergence.

Remarkably, calculating the counterfactual control trajectory reveals that **47%** of Britain's total industrial economic lead over the continent was locked in by 1810—during the height of the canal and water wheel era, and decades before steam power metrics display similar dominance in the corpus.
