# Abstract

The traditional chronology of the British Industrial Revolution credits fossil fuels—specifically coal extraction and the steam engine—as the primary catalysts that liberated human economics from the constraints of nature. This paper challenges the institutional "steam-first" narrative by isolating the quantitative macroeconomic impact of water infrastructure prior to the pervasive adoption of fossil extraction. By applying Natural Language Processing (NLP) to the historical Google Books `eng_gb_2019` corpus, we identify a structural shift wherein Britain's printed vocabulary transitioned from viewing water as a natural hazard to commodifying it as an engineered asset (the "Hydro-Social Shift").

Our analysis identifies 1766 as the crossover year of this linguistic transition. Deploying 1766 as the treatment threshold within a Difference-in-Differences (DiD) framework using Maddison Project historical GDP data, we estimate that this early hydro-social capitalization is associated with an additional $1,292 GDP per capita for Britain compared to continental European controls. Approximately 47% of Britain's ultimate industrial divergence was established during this "Water Era," decades before steam engines achieved commercial dominance. Placebo falsification tournaments across alternative industrial and agricultural sectors yield null effects, supporting the specificity of the water infrastructure channel. However, we acknowledge important limitations: the treatment year is derived endogenously from the linguistic corpus itself, the Google Books Ngram dataset carries known compositional biases, and our DiD framework captures association rather than definitive causation. Subject to these caveats, the data suggest a reframing of early modernity not as mankind's violent conquest of nature via fossil fuels, but rather as an era of "geographical symbiosis"—a cooperative capitalization of natural topographies and hydrology that preceded and potentially enabled the subsequent fossil transition.


---

# 1. Introduction

The origins of the British Industrial Revolution have been heavily debated, yet prominent perspectives often gravitate toward a singular technological rupture: the adoption of coal and the maturation of the steam engine. According to this narrative—deeply rooted in the *Unbound Prometheus* paradigm formalized by David S. Landes (1969) and enduring across both classical Marxist and neoclassical historiography—macroeconomic modernity accelerated significantly when economies broke free from the natural limitations of the organic economy by extracting subterranean fossil fuels. Within this framework, industrialization is frequently characterized philosophically and economically as humanity's uncoupling from, and mastery over, the natural environment.

This perspective is entrenched in the historiography of economic development. E.A. Wrigley famously conceptualized the Industrial Revolution as the necessary transition from an "organic economy"—limited by the photosynthetic capture of solar energy via wood and wind—to a "mineral-based energy economy" built on coal (Wrigley 2010). In his view, sustained exponential growth was physically impossible within the confines of organic flows. Similarly, Robert Allen's robust "High Wage Economy" thesis posits that Britain's unique matrix of cheap coal and high labor costs structurally induced the invention of the steam engine, treating geological luck as the prime engine of British divergence (Allen 2009).

However, this energy-centric perspective operates alongside equally foundational institutional and cultural theories. Deirdre McCloskey argues that an epistemological shift in rhetoric and culture—how society spoke about commerce and innovation—was a crucial prerequisite for industrialization (McCloskey 2010). Similarly, Joel Mokyr theorizes that exponential growth was unlocked by the systematic accumulation and application of "useful knowledge" (Mokyr 2009). Yet, unifying these cultural shifts with the material and energetic transitions of the period remains an ongoing methodological challenge.

Furthermore, the material realities of early manufacturing complicate the coal-centric timeline. The sprawling networks of navigable canals, aqueducts, and mechanized water wheels suggest that the foundation of the British economic trajectory was laid not by subverting the landscape via fossil extraction, but by actively partnering with it. Recent quantitative work has begun to substantiate this claim. Bogart et al. (2024) estimate that inter-urban freight transport costs in England declined by nearly 75% between 1680 and 1830 due to river improvements, canal construction, and road upgrades, and that without these reductions, inland towns would have been 20–25% smaller by 1841. Their findings demonstrate that early transport infrastructure—predominantly water-based—significantly shaped the spatial structure of urban economies during the First Industrial Revolution and beyond. As Andreas Malm argues in *Fossil Capital*, the eventual transition from water to steam power in the mid-19th century was not driven by thermodynamic superiority or absolute scarcity of water, but by the socio-spatial demands of capital. Steam engines allowed factories to be relocated to urban centers where labor could be disciplined, whereas water power required factories to adapt to remote riverine ecologies (Malm 2016). If the energetic foundation of modernity was actually established in the organic era, the timeline of industrialization is fundamentally late.

This paper tests the hypothesis that the linguistic commodification of water preceded the semantic integration of fossil fuels, and that this specific "First Mover" systemic advantage is associated with Britain's initial macroeconomic takeoff. By doing so, it seeks to serve as an empirical bridge between McCloskey's rhetoric, Mokyr's useful knowledge, and the tangible energetic realities of early infrastructure. We propose that the industrial mindset did not originate from the violent extraction of the earth, but from a cooperative, engineered integration with the natural hydrology of the British Isles.

Methodologically, we draw on two distinct traditions. First, the "culturomics" framework pioneered by Michel et al. (2011) demonstrated that massive digitized text corpora can reveal quantitative cultural trends across centuries. However, as Pechenick et al. (2015) have shown, the Google Books corpus carries significant compositional limitations—it functions more as a library catalogue than a representative sample of cultural discourse, and is increasingly dominated by scientific and technical texts from the 19th century onward. We design our vocabulary classification and smoothing procedures with these limitations in mind, though we acknowledge that corpus composition bias cannot be fully eliminated (see Section 5). Second, we employ Difference-in-Differences (DiD) econometric modeling, following the methodological standards reviewed in Roth et al. (2023), including event-study validation of parallel trends and placebo falsification exercises.

By deploying this dual-pronged computational methodology—merging natural language processing (NLP) of centuries of historical print culture with DiD econometric modeling of historical GDP—we explore the chronological timing of this linguistic "hydro-social shift." The findings encourage a reevaluation of not merely *when* the Industrial Revolution began in earnest, but *how* human integration with the natural world facilitated sustained growth. We offer quantitative evidence suggesting that the engineered cooperation with natural riverine environments—what we term "geographical symbiosis"—acted as an underappreciated macroeconomic catalyst of early modernity, preceding the widespread fossil fuel era by nearly a half-century.


---

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


---

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


---

# 4. Discussion

Our findings invite a reassessment of the prevailing institutional timeline that characterizes the Industrial Revolution primarily as a mineral energy transition. According to frameworks rooted in the mid-19th century fossil boom, sustained macroeconomic growth accelerated largely when economies began to decouple from natural ecosystems. This conceptual tethering traces directly back to classical political economy; as Karl Marx (1847) famously summarized, "the hand-mill gives you society with the feudal lord; the steam-mill, society with the industrial capitalist." Marx's mechanistic linkage of steam to the fundamental reorganization of human labor and capital cemented the assumption that true industrial modernity required the physical supremacy of the steam engine. Consequently, the prevailing paradigm continues to treat early geometric growth as uniquely dependent on the subversion of natural constraints via fossil extraction.

The 1766 hydro-social crossover complicates this narrative. A substantial proportion of Britain's ultimate early industrial divergence relative to continental Europe appears to have been established not through fossil extraction, but through advanced topographical engineering and ecological cooperation. The technological backbone of early modernity—the thousands of miles of navigable canals conforming to the earth's natural contours, and the massive water-wheels borrowing kinetic energy strictly from existing riverine flows—did not conquer the landscape; it collaborated with it. Recent empirical work reinforces this picture: Bogart et al. (2024) demonstrate that early transport improvements—primarily canals and river navigation—reduced freight costs by 75% and had persistent positive effects on urban population and property income well into the late 19th century.

The linguistic shift identified in our `eng_gb_2019` dataset signals a notable transformation in the British printing of technical vocabulary. Rather than perceiving water purely as a natural risk or hazard, early industrial society learned to harness topography. The conceptual framework transitioned from natural risk to what we term **geographical symbiosis**: a mode of economic development predicated on leveraging, rather than overriding, existing gravitational and hydrological constraints through engineered infrastructure. This framing is deliberately analytical rather than normative—we use "symbiosis" to denote the structural dependence of early industrial production on existing natural water flows, in contrast to the spatial liberation that steam later afforded.

This framing reinforces the analytical thesis of Terje Tvedt (2010), who argues that Britain's specific hydro-topographical endowments—and the infrastructural capacity to harness them for both kinetic energy and bulk transport—functioned as a critical precursor to the steam revolution. Rather than emerging in isolation, the steam engine can be viewed as an adaptive technology, encouraged by the expanding market scale that water infrastructure had fostered. By facilitating unprecedented logistical integration, canals and waterwheels aggregated complex supply chains and generated demand for continuous output. It is plausible that this hydro-social integration created systemic economic pressure for a spatially liberated prime mover. To sustain the volume of markets stimulated by these riparian networks, production ultimately expanded beyond the physical capacity of river valleys, encouraging the adoption of steam to allow geographically isolated capital and labor to participate more fully in the catalyzed economy.

Consequently, identifying water infrastructure as a significant factor in sustained economic growth encourages a reassessment of the timeline of industrialization. The empirical data point toward a distinct transitional phase: not exclusively the subsequent moment humanity transitioned to a mineral economy, but the preceding era where society embedded itself systematically into nature through infrastructural integration.

This empirically engages Malm's socio-spatial framing (Malm 2016). If the economic foundation of industrial divergence was substantially established in the organic era, then the eventual transition to coal and steam requires more than a strictly thermodynamic explanation. The hydro-social shift provides quantitative evidence that symbiotic scaling was economically viable in the pre-fossil period. The subsequent transition to fossil extraction can thus be viewed as a sociological and structural shift—driven by the spatial demands of concentrated labor markets—operating sequentially after the initial takeoff rather than inaugurating it.

We emphasize, however, that our evidence establishes temporal precedence and sectoral specificity, not definitive causal identification. The association between the hydro-social linguistic shift and GDP divergence is robust across specifications and survives placebo falsification, but the endogenous derivation of the treatment year prevents us from making the strong causal claims that a true natural experiment would permit. Future work employing exogenous variation—such as parliamentary canal acts or geological instruments for waterway navigability—could strengthen the causal architecture of these findings.


---

# 5. Limitations

Several important limitations qualify our findings and should guide their interpretation.

**Endogenous Treatment Year.** The most consequential limitation is that our treatment date ($T_0 = 1766$) is derived from the same cultural system whose economic effects we attempt to measure. Unlike a policy intervention, natural disaster, or regulatory change, the linguistic crossover is an emergent property of the socioeconomic transformation under study. This means our DiD framework identifies a structured temporal association—the hydro-social shift coincides with and precedes GDP divergence in a pattern that is unique to water vocabulary—but falls short of the strict exogeneity required for definitive causal inference. We partially address this through event-study validation (flat pre-trends), placebo vocabulary tournaments (null effects for rival sectors), and placebo-in-space tests (null effects for control countries), but acknowledge that these tests demonstrate specificity rather than causation per se.

**Google Books Corpus Composition.** As Pechenick et al. (2015) document, the Google Books corpus is compositionally uneven: it is more accurately described as a digitized library than a representative sample of cultural discourse. Scientific and technical texts constitute an increasing share of the corpus over time, which could mechanically inflate the frequency of engineering vocabulary irrespective of broader cultural trends. Our ratio-based approach (tracking the relative share of industrial vs. agrarian water terminology) partially mitigates this, since both lexicons would be affected by the general expansion of technical publishing. However, if industrial water texts were disproportionately represented in libraries relative to agrarian or religious texts, the crossover year could be biased earlier. The use of the `eng_gb_2019` British-specific sub-corpus reduces potential contamination from American English, but some non-British texts may remain (Greenfield 2016).

**Polysemy and Semantic Drift.** Several terms in our vocabulary arrays are polysemous. "Mill," "power," and "engine" carry meanings that extend well beyond water infrastructure. Although our iteration tracker documents robustness checks using unambiguous bigrams only (e.g., "water wheel," "inland navigation"), which yield consistent results ($p = 0.002$), the baseline specification using unigrams remains vulnerable to counting irrelevant uses. A full corpus-level disambiguation—such as the word embedding approach outlined in our Phase 2 research proposal—would substantially strengthen the linguistic identification.

**Low Baseline R² and Residual Autocorrelation.** The pooled OLS specification yields an $R^2$ of 0.214 and a Durbin-Watson statistic of 0.032, indicating that the model explains only a modest share of GDP variation and that residuals are highly autocorrelated. The low $R^2$ is expected in a parsimonious model applied to two centuries of GDP data across heterogeneous economies—most variation is absorbed by country-level baselines and secular time trends, which our two-way fixed effects specification captures ($R^2 = 0.884$). The extreme autocorrelation is inherent to annual macroeconomic time series spanning 200 years; we address this via Newey-West HAC standard errors (lag=3) following Bertrand, Duflo, and Mullainathan (2004), but acknowledge that alternative approaches—such as clustering at the country level or collapsing the data into longer time periods—could yield different inference.

**Interpolated GDP Data.** The Maddison Project provides near-complete annual data for Great Britain, France, and the Netherlands, but China and India rely on substantially more interpolation from sparse benchmark estimates. Linear interpolation between benchmarks mechanically smooths the GDP series for these countries, potentially masking short-run dynamics. For this reason, we treat the European DiD as our primary specification and the Asian comparisons as supplementary.

**Print Culture as Proxy for Society.** The linguistic analysis measures shifts in published vocabulary, not in the material economy directly. The endogeneity of print culture (tracker item #7) remains unresolved: the surge in water-engineering terminology may reflect, rather than drive, the underlying infrastructure boom. Our framework is consistent with both interpretations—the linguistic shift as a leading cultural indicator, or as a contemporaneous reflection of material change—and we do not claim to distinguish between these channels.


---

# 6. Conclusion

This paper provides empirical evidence that refines the technological and macroeconomic timeline of early modernity. By merging natural language processing on historical print corpora with formal difference-in-differences economic modeling, we identify a structured temporal association between the cultural commodification of water and the origins of British industrial divergence.

We find that an early phase of British macroeconomic acceleration is closely linked to the 1766 "Hydro-Social Shift"—the point at which British print culture structurally embraced water as an engineered industrial asset rather than a natural hazard. The estimated ~$1,292 per capita GDP advantage relative to continental peers was established significantly prior to the widespread commercialization of fossil power. By testing parallel trends and executing placebo falsification exercises against textile, coal, and financial vocabulary, the analysis accounts for general industrial expansion and highlights the distinct association of hydro-infrastructure with early divergence.

These findings carry important caveats. The treatment year is derived endogenously, the Google Books corpus is compositionally imperfect, and our framework captures temporal association rather than definitive causation. Nevertheless, the specificity of the water channel—surviving placebo tests that eliminate rival sectors—and the clean parallel trends in the event study suggest that the hydro-social shift captures a genuine structural feature of early British industrialization, not a statistical artifact.

If these findings withstand further scrutiny, they carry implications beyond economic history. The early macroeconomic acceleration of the British economy appears grounded in an era of geographical symbiosis—a period of intense infrastructural cooperation with the natural environment—rather than resting exclusively on fossil extraction. This reframing suggests that the relationship between economic growth and ecological systems in early modernity was more collaborative than the dominant fossil-first narrative implies, and that the transition to steam may be better understood as a structural shift in the spatial organization of capital than as the inaugural moment of industrial growth itself.

Future work should pursue three priorities: (i) exploiting exogenous variation in canal construction (e.g., parliamentary canal acts, geological instruments for waterway navigability) to strengthen causal identification; (ii) extending the linguistic analysis to full-text corpora such as HathiTrust, enabling word embedding and topic modeling approaches that can disambiguate polysemous terms; and (iii) comparative analysis of equivalent corpora for France and the Netherlands to test whether the absence of a hydro-social shift in control economies aligns with their relatively later industrialization.


---

# References

Allen, Robert C. 2009. *The British Industrial Revolution in Global Perspective*. Cambridge: Cambridge University Press.

Bertrand, Marianne, Esther Duflo, and Sendhil Mullainathan. 2004. "How Much Should We Trust Differences-in-Differences Estimates?" *Quarterly Journal of Economics* 119 (1): 249–75.

Bogart, Dan, Xuesheng You, Eduard J. Alvarez-Palau, Max Satchell, and Leigh Shaw-Taylor. 2024. "Transport and Urban Growth in the First Industrial Revolution." *The Economic Journal* 134 (662): 2168–2206.

Bolt, Jutta, and Jan Luiten van Zanden. 2020. "Maddison style estimates of the evolution of the world economy. A new 2020 update." *Maddison-Project Working Paper*, WP-154.

Broadberry, Stephen, Bruce M. S. Campbell, Alexander Klein, Mark Overton, and Bas van Leeuwen. 2015. *British Economic Growth, 1270–1870*. Cambridge: Cambridge University Press.

Crafts, Nicholas F. R. 1985. *British Economic Growth during the Industrial Revolution*. Oxford: Clarendon Press.

Landes, David S. 1969. *The Unbound Prometheus: Technological Change and Industrial Development in Western Europe from 1750 to the Present*. Cambridge: Cambridge University Press.

Malm, Andreas. 2016. *Fossil Capital: The Rise of Steam Power and the Roots of Global Warming*. London: Verso.

Marx, Karl. (1847) 1955. *The Poverty of Philosophy*. Moscow: Progress Publishers.

McCloskey, Deirdre N. 2010. *Bourgeois Dignity: Why Economics Can't Explain the Modern World*. Chicago: University of Chicago Press.

Michel, Jean-Baptiste, Yuan Kui Shen, Aviva Presser Aiden, Adrian Veres, Matthew K. Gray, and Erez Lieberman Aiden. 2011. "Quantitative Analysis of Culture Using Millions of Digitized Books." *Science* 331 (6014): 176–82.

Mokyr, Joel. 2009. *The Enlightened Economy: An Economic History of Britain 1700-1850*. New Haven: Yale University Press.

Pechenick, Eitan Adam, Christopher M. Danforth, and Peter Sheridan Dodds. 2015. "Characterizing the Google Books Corpus: Strong Limits to Inferences of Socio-Cultural and Linguistic Evolution." *PLoS ONE* 10 (10): e0137041.

Pomeranz, Kenneth. 2000. *The Great Divergence: China, Europe, and the Making of the Modern World Economy*. Princeton: Princeton University Press.

Roth, Jonathan, Pedro H. C. Sant'Anna, Alyssa Bilinski, and John Poe. 2023. "What's Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature." *Journal of Econometrics* 235 (2): 2218–44.

Tvedt, Terje. 2010. "Why England and not China and India? Water Systems and the History of the Industrial Revolution." *Journal of Global History* 5 (1): 29–50.

Wrigley, E. A. 2010. *Energy and the English Industrial Revolution*. Cambridge: Cambridge University Press.


---

