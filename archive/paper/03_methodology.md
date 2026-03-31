# 3. Methodology

To quantitatively map the hydro-social shift, this paper deploys a two-phase computational methodology merging cultural linguistic text analysis with applied econometrics. 

### 3.1 Unsupervised Natural Language Processing (Google Books Corpus)
The first phase isolates when and how "water" transitioned culturally from an uncontrollable natural phenomenon to an infrastructural utility within the British lexicon. Using the `eng_gb_2019` Google Books Ngram corpus, we track the historical trajectories of a curated array of 71 terms ranging from 1700 to 1900. 

These terms are divided into two primary matrices:
1. **The Natural/Religious Lexicon:** (e.g., *flood, tempest, divine water, hazard*)
2. **The Engineered/Commodified Lexicon:** (e.g., *water wheel, navigable canal, mill race, aqueduct*)

Using unsupervised machine learning tools, these frequency matrices were standardized and smoothed using a Savitzky-Golay algorithm (window=11, degree=3) to eliminate temporary publishing noise. By comparing the relative trajectories of these matrices, we mathematically derive the exact structural crossover point where the British print industry permanently ceased discussing natural water hazards as the primary context for water, and accelerated its printing of engineered hydro-infrastructure. The resulting structural crossover year ($T_0=1766$) serves as the precise historical treatment intervention. 

### 3.1 Data Construction
The analysis depends on two primary datasets:
1. **Google Books Ngram Corpus (English GB 2019):** Extracting annual frequencies of specifically compiled lexicons (`water_wheel`, `canal` vs. `steam_engine`, `coal`) from 1700 to 1900. By deploying this text-as-data approach, we build directly upon the methodological foundations of quantitative culturomics established by Michel et al. (2011).
2. **Macroeconomic GDP Series:** Sourced from the Maddison Project Database (Bolt and van Zanden 2020), which aggregates pre-industrial growth accounting from pioneering works like Crafts (1985) and the definitive historical GDP reconstructions of Broadberry et al. (2015). We provide continuous annual GDP per capita estimates for Britain, matched against France, the Netherlands, China, and India. The inclusion of the latter two non-European controls directly engages the "Great Divergence" debate formalized by Kenneth Pomeranz (2000), allowing us to cleanly measure the timing of Britain's escape from the Malthusian constraints of its peers.

### 3.2 Econometric Merge (Difference-in-Differences)
To explicitly test the causal correlation between this cultural phenomenon and exponential geometric growth—the hallmark of macroeconomic modernity—the 1766 structural shift is overlaid onto real historical GDP data from the Maddison Project Database (Bolt and van Zanden 2020). 

We construct a multi-specification Difference-in-Differences (DiD) model treating Great Britain as the primary experimental group, using France and the Netherlands as contemporary 18th-century European controls. Formally, our baseline Two-Way Fixed Effects (TWFE) DiD specification is estimated as:

$$ Y_{it} = \alpha + \beta (\text{GBR}_i \times \text{Post}_{t}) + \gamma_i + \delta_t + \epsilon_{it} $$

Where $Y_{it}$ represents the continuous metric (GDP per capita or Log GDP per capita) for country $i$ in year $t$. The variable $\text{GBR}_i$ is the treatment dummy equal to 1 for Great Britain, and $\text{Post}_t$ is the indicator variable equal to 1 for the post-crossover environment ($t \ge 1766$). The parameters $\gamma_i$ and $\delta_t$ represent country and year fixed effects, respectively, which absorb unobserved cultural/geographical baselines and global structural shocks. The interaction coefficient $\beta$ identifies the overarching hydro-social divergence effect. Serial autocorrelation, standard in multi-century economic datasets, is resolved via Newey-West HAC robust standard errors ($\text{lag}=3$).

This methodology strictly bounds the investigation to ensure causal validity. Pre-treatment parallel trends are explicitly validated using a dynamic event-study specification to map the precise temporal evolution of the treatment effect:

$$ Y_{it} = \alpha + \sum_{k=-K}^{L} \beta_k (\text{GBR}_i \times \mathbb{I}(t = 1766 + k)) + \gamma_i + \delta_t + \epsilon_{it} $$

Where the coefficients $\beta_k$ isolate the dynamic divergence using 5-year binned increments ($k$) relative to the structural break. This formal methodology mathematically rules out pre-existing trajectory bias (testing that $\beta_k = 0$ for $k < 0$), ensuring that the British geometric takeoff did not autonomously precede the hydro-social shift, but was catalyzed strictly concurrently with it. Finally, iterating the $T_0$ thresholds in the event study matrix across the linguistic trajectories of *textiles*, *coal*, and *finance* establishes a distinct placebo falsification tournament, guaranteeing the absolute causal integrity of water infrastructure.
