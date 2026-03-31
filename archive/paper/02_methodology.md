# 2. Methodology

To quantitatively map the hydro-social shift, this paper deploys a two-phase computational methodology merging cultural linguistic text analysis with applied econometrics.

### 2.1 Linguistic Classification (Google Books Corpus)
The first phase isolates when and how "water" transitioned culturally from an uncontrollable natural phenomenon to an infrastructural utility within the British lexicon. Using the `eng_gb_2019` Google Books Ngram corpus, we track the historical trajectories of a curated array of 71 terms ranging from 1700 to 1900.

These terms are divided into two primary matrices:
1. **The Natural/Religious Lexicon:** (e.g., *flood, tempest, divine water, hazard*)
2. **The Engineered/Commodified Lexicon:** (e.g., *water wheel, navigable canal, mill race, aqueduct*)

These frequency matrices were standardized and smoothed using a Savitzky-Golay algorithm (window=11, degree=3) to eliminate temporary publishing noise. By comparing the relative trajectories of these matrices, we derive the structural crossover point where the British print industry ceased discussing natural water hazards as the primary context for water, and accelerated its printing of engineered hydro-infrastructure. The resulting structural crossover year ($T_0=1766$) serves as the historical treatment intervention.

An important methodological caveat applies: as Pechenick et al. (2015) demonstrate, the Google Books corpus is compositionally uneven—it is more accurately described as a library than as a representative sample of cultural discourse. Scientific and technical publications constitute an increasing share of the corpus from the late 18th century onward, which could mechanically inflate the frequency of engineering terminology. We mitigate this partially through our balanced vocabulary design (tracking both natural and industrial terms as a ratio rather than raw frequencies) and through Savitzky-Golay smoothing, but acknowledge that corpus composition effects cannot be fully controlled. The `eng_gb_2019` British-specific sub-corpus reduces but does not eliminate potential contamination from non-British English texts (see Limitations, Section 5).

### 2.2 Data Construction
The analysis depends on two primary datasets:
1. **Google Books Ngram Corpus (English GB 2019):** Extracting annual frequencies of specifically compiled lexicons (`water_wheel`, `canal` vs. `steam_engine`, `coal`) from 1700 to 1900. By deploying this text-as-data approach, we build directly upon the methodological foundations of quantitative culturomics established by Michel et al. (2011).
2. **Macroeconomic GDP Series:** Sourced from the Maddison Project Database (Bolt and van Zanden 2020), which aggregates pre-industrial growth accounting from pioneering works like Crafts (1985) and the definitive historical GDP reconstructions of Broadberry et al. (2015). We provide continuous annual GDP per capita estimates for Britain, matched against France, the Netherlands, China, and India. The inclusion of the latter two non-European controls directly engages the "Great Divergence" debate formalized by Kenneth Pomeranz (2000), allowing us to measure the timing of Britain's escape from the Malthusian constraints of its peers.

### 2.3 Control Group Selection
France and the Netherlands serve as our primary European control group. This selection is motivated by three criteria: (i) both economies were broadly comparable to Britain in the early 18th century in terms of GDP per capita, urbanization, and maritime commercial activity; (ii) both possessed navigable waterway infrastructure but did not undergo the same concentrated canal-building boom as Britain between 1760 and 1830; and (iii) the Maddison Project provides near-complete annual GDP data for both countries across the full 1700–1900 window, minimizing interpolation artifacts. China and India are included as supplementary non-European controls to engage the "Great Divergence" literature, though their GDP series require substantially more interpolation from sparse benchmarks and are therefore treated as secondary.

### 2.4 Econometric Framework (Difference-in-Differences)
To test whether the linguistic commodification of water is associated with Britain's macroeconomic divergence, the 1766 structural shift is overlaid onto real historical GDP data from the Maddison Project Database (Bolt and van Zanden 2020).

We construct a multi-specification Difference-in-Differences (DiD) model treating Great Britain as the treatment group, using France and the Netherlands as contemporary 18th-century European controls. Formally, our baseline Two-Way Fixed Effects (TWFE) DiD specification is estimated as:

$$ Y_{it} = \alpha + \beta (\text{GBR}_i \times \text{Post}_{t}) + \gamma_i + \delta_t + \epsilon_{it} $$

Where $Y_{it}$ represents the continuous metric (GDP per capita or Log GDP per capita) for country $i$ in year $t$. The variable $\text{GBR}_i$ is the treatment dummy equal to 1 for Great Britain, and $\text{Post}_t$ is the indicator variable equal to 1 for the post-crossover environment ($t \ge 1766$). The parameters $\gamma_i$ and $\delta_t$ represent country and year fixed effects, respectively, which absorb unobserved cultural/geographical baselines and global structural shocks. The interaction coefficient $\beta$ identifies the hydro-social divergence effect. Following the recommendations of Bertrand, Duflo, and Mullainathan (2004) for long panels, serial autocorrelation is addressed via Newey-West HAC robust standard errors ($\text{lag}=3$).

We note that the baseline pooled specification (without two-way fixed effects) yields an $R^2$ of 0.214. This reflects the inherent difficulty of explaining multi-century GDP variation across heterogeneous economies with a single binary treatment. The two-way fixed effects specification absorbs country-level baselines and global time trends, raising the $R^2$ to 0.884. Both specifications yield a consistent and statistically significant DiD coefficient, suggesting that the treatment effect is robust to model specification rather than an artifact of omitted heterogeneity.

Pre-treatment parallel trends are validated using a dynamic event-study specification to map the temporal evolution of the treatment effect:

$$ Y_{it} = \alpha + \sum_{k=-K}^{L} \beta_k (\text{GBR}_i \times \mathbb{I}(t = 1766 + k)) + \gamma_i + \delta_t + \epsilon_{it} $$

Where the coefficients $\beta_k$ isolate the dynamic divergence using 5-year binned increments ($k$) relative to the structural break. This methodology tests for pre-existing trajectory bias ($\beta_k = 0$ for $k < 0$), following the event-study validation framework reviewed in Roth et al. (2023). Finally, iterating the $T_0$ thresholds across the linguistic trajectories of *textiles*, *coal*, and *finance* establishes a placebo falsification tournament to assess the specificity of the water infrastructure channel.

A critical identification concern must be acknowledged: unlike a natural experiment or policy shock, the treatment year $T_0 = 1766$ is derived endogenously from the same cultural system under study. The linguistic crossover is not an exogenous intervention imposed on Britain from outside, but rather an emergent property of the very socioeconomic transformation we seek to measure. This means our DiD framework captures a structured temporal association between the hydro-social linguistic shift and GDP divergence, rather than establishing causation in the strict interventionist sense. The event study and placebo tests strengthen the case for specificity—the association is unique to water vocabulary and absent for rival sectors—but cannot fully resolve the endogeneity of the treatment date.
