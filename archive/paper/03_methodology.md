# 3. Methodology

To quantitatively map the hydro-social shift, this paper deploys a two-phase computational methodology merging cultural linguistic text analysis with applied econometrics. 

### 3.1 Unsupervised Natural Language Processing (Google Books Corpus)
The first phase isolates when and how "water" transitioned culturally from an uncontrollable natural phenomenon to an infrastructural utility within the British lexicon. Using the `eng_gb_2019` Google Books Ngram corpus, we track the historical trajectories of a curated array of 71 terms ranging from 1700 to 1900. 

These terms are divided into two primary matrices:
1. **The Natural/Religious Lexicon:** (e.g., *flood, tempest, divine water, hazard*)
2. **The Engineered/Commodified Lexicon:** (e.g., *water wheel, navigable canal, mill race, aqueduct*)

Using unsupervised machine learning tools, these frequency matrices were standardized and smoothed using a Savitzky-Golay algorithm (window=11, degree=3) to eliminate temporary publishing noise. By comparing the relative trajectories of these matrices, we derive the structural crossover point where the British print industry shifted from discussing natural water hazards as the primary context for water toward the language of engineered hydro-infrastructure. The resulting structural crossover year occurred in 1766. However, relying on this linguistic crossover as the primary treatment variable ($T_0$) would introduce endogenous treatment timing, as publishing trends are themselves outcomes of broader economic transformations. 

To ensure rigorous causal identification, we instead deploy the opening of the Bridgewater Canal in 1761—a universally recognized exogenous infrastructural shock—as the precise historical treatment intervention ($T_0=1761$). The 1766 linguistic crossover thus serves as an independent "mechanism validator," confirming that the exogenous 1761 physical shock catalyzed a measurable cultural shift five years later. 

### 3.2 Vocabulary Construction
The 71 vocabulary terms are organized into six analytically distinct categories, each designed to capture a specific dimension of the hypothesized hydro-social transformation:

1. **Core hydro-infrastructure** (4 terms): *water, canal, mill, pump* — high-frequency terms capturing the broadest contour of water's industrial role.
2. **Period-specific water technology** (18 terms): *water wheel, overshot, undershot, water mill, mill wheel, breast wheel, water power, water frame, water engine, mill race, sluice, penstock, cotton mill, spinning mill, corn mill, fulling mill, inland navigation, canal navigation* — drawn from period-appropriate engineering vocabulary documented in primary sources.
3. **Canal transport infrastructure** (6 terms): *navigable, barge, towpath, waterway, inland navigation, canal navigation* — capturing the logistics revolution that canals enabled.
4. **Naturalistic/agrarian baseline** (6 terms): *flood, rain, river, harvest, holy, divine* — representing the pre-industrial conceptualization of water as natural phenomenon or divine force.
5. **Fossil/steam comparators** (3 terms): *steam, coal, engine* — enabling direct temporal comparison with the conventional "Promethean" narrative.
6. **Placebo categories** (20 terms across five rival hypotheses): coal mining, textile, financial, agricultural, and steam-mechanical vocabularies — each representing an alternative explanation for the Great Divergence, used in falsification tournaments.

The selection of terms was guided by three criteria: documented usage in 18th-century primary sources (parliamentary acts, engineering treatises, commercial directories), sufficient frequency in the Ngram corpus to produce stable annual estimates, and analytical distinctiveness (terms should not be semantically redundant within their category). While the vocabulary selection is ultimately heuristic, the placebo tournament design mitigates term-selection bias by demonstrating that rival vocabularies — constructed with equivalent care — fail to produce comparable event study patterns.

### 3.3 Data Construction
The analysis depends on two primary datasets:
1. **Google Books Ngram Corpus (English GB 2019):** Extracting annual frequencies of specifically compiled lexicons (`water_wheel`, `canal` vs. `steam_engine`, `coal`) from 1700 to 1900. By deploying this text-as-data approach, we build directly upon the methodological foundations of quantitative culturomics established by Michel et al. (2011). We use the British English sub-corpus (`eng_gb_2019`) rather than the general English corpus to isolate British intellectual culture from American and colonial contributions that increasingly dominate the general corpus after 1800.
2. **Macroeconomic GDP Series:** Sourced from the Maddison Project Database (Bolt and van Zanden 2020), which aggregates pre-industrial growth accounting from pioneering works like Crafts (1985) and the definitive historical GDP reconstructions of Broadberry et al. (2015). We provide continuous annual GDP per capita estimates (in 2011 international dollars) for Britain, matched against an expanded panel of 12 control countries. The primary European controls — France and the Netherlands — share comparable institutional development, maritime trade exposure, and Enlightenment intellectual traditions, isolating the treatment effect of Britain's unique water infrastructure endowment. An extended European panel adds Belgium, Sweden, Germany, Spain, Portugal, Poland, and Italy, substantially increasing cross-sectional variation and statistical power. China, India, and Japan serve as extended "Great Divergence" controls, directly engaging the framework formalized by Pomeranz (2000). Spain, Portugal, and Poland provide particularly dense pre-treatment coverage (61+ annual observations before 1761), strengthening inference on pre-treatment parallel trends.

### 3.4 Econometric Merge (Difference-in-Differences)
To explicitly test the structural association between this cultural phenomenon and sustained economic growth, the 1761 exogenous shock is overlaid as the treatment variable onto real historical GDP data from the Maddison Project Database (Bolt and van Zanden 2020). 

We construct a multi-specification Difference-in-Differences (DiD) model treating Great Britain as the primary experimental group, using France and the Netherlands as contemporary 18th-century European controls. Formally, our baseline Two-Way Fixed Effects (TWFE) DiD specification is estimated as:

$$ Y_{it} = \alpha + \beta (\text{GBR}_i \times \text{Post}_{t}) + \gamma_i + \delta_t + \epsilon_{it} $$

Where $Y_{it}$ represents the continuous metric (GDP per capita or Log GDP per capita) for country $i$ in year $t$. The variable $\text{GBR}_i$ is the treatment dummy equal to 1 for Great Britain, and $\text{Post}_t$ is the indicator variable equal to 1 for the post-shock environment ($t \ge 1761$). The parameters $\gamma_i$ and $\delta_t$ represent country and year fixed effects, respectively, which absorb unobserved cultural/geographical baselines and global structural shocks. The interaction coefficient $\beta$ identifies the hydro-social divergence effect. Serial autocorrelation, standard in multi-century economic datasets, is addressed via Newey-West HAC robust standard errors ($\text{lag}=15$).

This methodology strictly bounds the temporal investigation. Pre-treatment parallel trends are validated using a dynamic event-study specification to map the temporal evolution of the structural break:

$$ Y_{it} = \alpha + \sum_{k=-K}^{L} \beta_k (\text{GBR}_i \times \mathbb{I}(t = 1761 + k)) + \gamma_i + \delta_t + \epsilon_{it} $$

Where the coefficients $\beta_k$ isolate the dynamic divergence using 5-year binned increments ($k$) relative to the structural break. This specification tests for pre-existing trajectory bias ($\beta_k = 0$ for $k < 0$), verifying that the British economic takeoff did not autonomously precede the infrastructural shift, but coincided sequentially with it. Finally, iterating the $T_0$ thresholds in the event study matrix across the linguistic trajectories of *textiles*, *coal*, and *finance* establishes a placebo falsification tournament, testing whether the statistical alignment of the 1761 structural break is uniquely associated with water vocabulary rather than a generic artifact of 18th-century development.

### 3.5 Double/Debiased Machine Learning (DML)

As an independent robustness check on the DiD results, we implement the partially linear Double/Debiased Machine Learning estimator of Chernozhukov et al. (2018). This approach estimates:

$$ Y_{it} = \theta \cdot D_{it} + g(X_{it}) + \varepsilon_{it} $$

where the treatment $D_{it}$ is the continuous hydro-social vocabulary intensity interacted with the Britain indicator ($D_{it} = \text{vocab\_intensity}_t \times \mathbf{1}[\text{GBR}_i]$), and $g(\cdot)$ is an unknown function of confounders $X$ estimated by machine learning. The partial-out procedure follows Frisch-Waugh-Lovell logic: ML models separately residualize $Y$ and $D$ on $X$ using $K$-fold cross-fitting ($K=5$), and $\theta$ is recovered by regressing the $Y$-residual on the $D$-residual.

**Confounders and identification.** Confounders $X$ include country fixed effects and a quadratic year trend. Critically, vocabulary intensity itself is excluded from $X$: including it alongside the Britain country dummy would allow the ML to reconstruct $D = \text{vocab\_intensity} \times \mathbf{1}[\text{GBR}]$ almost perfectly, collapsing the treatment residual to zero and rendering the estimator uninformative. This exclusion is the correct identification choice — vocabulary intensity is the treatment mechanism, not a confounder.

**Standard errors.** We report both naive Neyman-orthogonal standard errors and cluster-robust standard errors grouped by country. Since all treatment variation originates from a single country (Britain), the cluster-robust SE is the honest inferential quantity; naive SEs exploit cross-observation independence within Britain's time series and should be treated as a lower bound.

**Mediation test.** To test the enabling sequence water → steam → GDP, we run a second specification that adds raw steam vocabulary intensity to $X$ while retaining water vocabulary as the treatment. If water's GDP effect diminishes substantially when steam is controlled, this is consistent with water operating as a precondition *for* steam rather than as an independent rival channel.

**ML methods.** We implement four learners — Lasso, Ridge, Random Forest, and Gradient Boosting — and report results for each. Gradient Boosting, which flexibly controls for nonlinear year trends, is the preferred specification; linear methods (Lasso, Ridge) produce inflated $\hat{\theta}$ because they cannot fully absorb the nonlinear vocabulary time trend, leaving residual correlation between year and treatment that biases the estimate upward.
