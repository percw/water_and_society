# 3. Methodology

To quantitatively map the hydro-social shift, this paper deploys a two-phase computational methodology merging cultural linguistic text analysis with applied econometrics. 

### 3.1 Unsupervised Natural Language Processing (Google Books Corpus)
The first phase isolates when and how "water" transitioned culturally from an uncontrollable natural phenomenon to an infrastructural utility within the British lexicon. Using the `eng_gb_2019` Google Books Ngram corpus, we track the historical trajectories of a curated array of 71 terms ranging from 1700 to 1900. 

These terms are divided into two primary matrices:
1. **The Natural/Religious Lexicon:** (e.g., *flood, tempest, divine water, hazard*)
2. **The Engineered/Commodified Lexicon:** (e.g., *water wheel, navigable canal, mill race, aqueduct*)

Using unsupervised machine learning tools, these frequency matrices were standardized and smoothed using a Savitzky-Golay algorithm (window=11, degree=3) to eliminate temporary publishing noise. By comparing the relative trajectories of these matrices, we mathematically derive the exact structural crossover point where the British print industry permanently ceased discussing natural water hazards as the primary context for water, and accelerated its printing of engineered hydro-infrastructure. The resulting structural crossover year occurred in 1766. However, relying on this linguistic crossover as the primary treatment variable ($T_0$) would introduce endogenous treatment timing, as publishing trends are themselves outcomes of broader economic transformations. 

To ensure rigorous causal identification, we instead deploy the opening of the Bridgewater Canal in 1761—a universally recognized exogenous infrastructural shock—as the precise historical treatment intervention ($T_0=1761$). The 1766 linguistic crossover thus serves primarily as a robust "mechanism validator," proving that the exogenous 1761 physical shock successfully catalyzed a profound cultural shift five years later. 

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
2. **Macroeconomic GDP Series:** Sourced from the Maddison Project Database (Bolt and van Zanden 2020), which aggregates pre-industrial growth accounting from pioneering works like Crafts (1985) and the definitive historical GDP reconstructions of Broadberry et al. (2015). We provide continuous annual GDP per capita estimates for Britain, matched against France, the Netherlands, China, and India. France and the Netherlands serve as European controls sharing comparable institutional development, maritime trade exposure, and Enlightenment intellectual traditions — isolating the treatment effect of Britain's unique water infrastructure endowment. China and India serve as extended "Great Divergence" controls, directly engaging the framework formalized by Pomeranz (2000) and allowing us to cleanly measure the timing of Britain's escape from the Malthusian constraints of its Asian peers.

### 3.4 Econometric Merge (Difference-in-Differences)
To explicitly test the structural association between this cultural phenomenon and exponential geometric growth—the hallmark of macroeconomic modernity—the 1761 exogenous shock is overlaid as the treatment variable onto real historical GDP data from the Maddison Project Database (Bolt and van Zanden 2020). 

We construct a multi-specification Difference-in-Differences (DiD) model treating Great Britain as the primary experimental group, using France and the Netherlands as contemporary 18th-century European controls. Formally, our baseline Two-Way Fixed Effects (TWFE) DiD specification is estimated as:

$$ Y_{it} = \alpha + \beta (\text{GBR}_i \times \text{Post}_{t}) + \gamma_i + \delta_t + \epsilon_{it} $$

Where $Y_{it}$ represents the continuous metric (GDP per capita or Log GDP per capita) for country $i$ in year $t$. The variable $\text{GBR}_i$ is the treatment dummy equal to 1 for Great Britain, and $\text{Post}_t$ is the indicator variable equal to 1 for the post-shock environment ($t \ge 1761$). The parameters $\gamma_i$ and $\delta_t$ represent country and year fixed effects, respectively, which absorb unobserved cultural/geographical baselines and global structural shocks. The interaction coefficient $\beta$ identifies the overarching hydro-social divergence effect. Serial autocorrelation, standard in multi-century economic datasets, is resolved via Newey-West HAC robust standard errors ($\text{lag}=3$).

This methodology strictly bounds the temporal investigation. Pre-treatment parallel trends are validated using a dynamic event-study specification to uniquely map the precise temporal evolution of the structural break:

$$ Y_{it} = \alpha + \sum_{k=-K}^{L} \beta_k (\text{GBR}_i \times \mathbb{I}(t = 1761 + k)) + \gamma_i + \delta_t + \epsilon_{it} $$

Where the coefficients $\beta_k$ isolate the dynamic divergence using 5-year binned increments ($k$) relative to the structural break. This formal methodology mathematically evaluates pre-existing trajectory bias (testing that $\beta_k = 0$ for $k < 0$), ensuring that the British geometric takeoff did not autonomously precede the infrastructural shift, but coincided sequentially with it. Finally, iterating the $T_0$ thresholds in the event study matrix across the linguistic trajectories of *textiles*, *coal*, and *finance* establishes a distinct placebo falsification tournament, guaranteeing that the statistical alignment of the 1761 structural break is not a generic artifact of 18th-century development.
