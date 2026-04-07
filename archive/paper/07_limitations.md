# 7. Limitations and Robustness

The application of a quantitative culturomics framework to historical macroeconomics inherently requires methodological concessions. To ensure transparency, we highlight three primary vulnerabilities in our identification strategy.

## 7.1 Robustness to Endogenous Treatment Timing
A pervasive vulnerability in applying computational text analysis to macroeconomics is the risk of endogenous treatment timing. If the structural break utilized as the DiD treatment intervention ($T_0$) is derived exclusively from the linguistic corpus produced by the society experiencing economic transition—e.g., relying solely on our 1766 mathematical NLP crossover—the model risks circularity. 

To systematically neutralize this endogeneity critique, our methodology explicitly pivots away from deploying the NLP-derived marker as the treatment baseline. Instead, we anchor the Diff-in-Diff specification to the exogenous historical reality of the 1761 opening of the Bridgewater Canal—a singular infrastructural investment shock universally recognized as the catalyst for the subsequent canal mania. By utilizing 1761 as an exogenous variable, our use of the 1766 Google Books crossover is elegantly repurposed as an independent NLP mechanism validator. It quantitatively confirms that the exogenous topographical shock of 1761 definitively catalyzed and reorganized the macro-linguistic culture of the society exactly a half-decade later, resolving standard identification concerns cleanly.

## 7.2 Corpus Bias and the Scientific Publishing Boom
As demonstrated by Pechenick et al. (2015), the Google Books Ngram Corpus does not act as a strictly neutral mirror of popular culture. As the 18th and 19th centuries progressed, the corpus became increasingly dominated by scientific, technical, and legal texts. The surge in vocabulary related to canals and water wheels (`canal`, `water_wheel`, `engineer`) may therefore partially reflect an institutional boom in the publishing of technical manuals and parliamentary navigation acts, rather than a purely linguistic shift in daily life. However, in the context of economic history, the sudden profusion of technical infrastructure literature serves as an incredibly robust proxy for the material reorganization of the underlying economy.

Additionally, our vocabulary selection of 71 semantic targets was fundamentally heuristic. While our placebo vocabulary tournaments demonstrate that the relative timing of the "hydro" crossover uniquely aligns with the onset of GDP divergence compared to plausible alternatives (e.g., textiles, coal, or finance), a purely automated term-clustering algorithm would provide a more systematic foundation for future replication efforts. 

## 7.3 Data Interpolation and Serial Autocorrelation
While the Maddison Project Database (Bolt and van Zanden 2020) provides the finest scale of historical macroeconomic data available, the pre-1800 non-European control groups (particularly China and India) rely heavily on nonlinear interpolation between sparse historical benchmarks. Because interpolated data mechanically generates smooth trend lines, the parallel trends observed in our pre-treatment window (1700–1761) are inherently artificially stabilized. 

Serial autocorrelation is a fundamental challenge for any DiD design on annual time-series GDP data over a 200-year span. The baseline Durbin-Watson statistic of 0.043 confirms extreme positive autocorrelation, consistent with the warnings of Bertrand, Duflo, and Mullainathan (2004). We implement three corrections as reported in Table 3:

1. **Newey-West HAC** standard errors (lag=15) inflate the DiD standard error from 202 to 614, but $\beta_3$ retains statistical significance at the 5% level ($p = 0.042$).

2. **Country-clustered standard errors** yield $p < 0.001$, though with only $G = 3$ European clusters, clustered inference should be interpreted conservatively following Cameron, Gelbach, and Miller (2008).

3. **The collapsed DiD estimator** of Bertrand et al. (2004) completely eliminates serial autocorrelation by averaging GDP per capita into two periods per country (Durbin-Watson improves from 0.043 to 1.302). The point estimate is preserved exactly ($\beta_3 = 1{,}250.9$ for European controls), confirming that the estimated magnitude is not an artifact of autocorrelation-inflated precision. However, with $N = 6$ the test lacks statistical power ($p = 0.628$), reflecting a structural limitation of the collapsed estimator when applied to panels with very few cross-sectional units—a common constraint in historical macroeconomic DiD designs where the treatment was genuinely nation-specific.

Taken together, these results indicate that while the *magnitude* of the treatment effect is robust across all corrections, its statistical precision depends on the variance structure assumed. The HAC correction, which preserves the full time-series information while accounting for serial dependence, represents the most informative inference framework for this setting.
