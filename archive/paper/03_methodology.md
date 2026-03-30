# 3. Methodology

To quantitatively map the hydro-social shift, this paper deploys a two-phase computational methodology merging cultural linguistic text analysis with applied econometrics. 

### 3.1 Unsupervised Natural Language Processing (Google Books Corpus)
The first phase isolates when and how "water" transitioned culturally from an uncontrollable natural phenomenon to an infrastructural utility within the British lexicon. Using the `eng_gb_2019` Google Books Ngram corpus, we track the historical trajectories of a curated array of 71 terms ranging from 1700 to 1900. 

These terms are divided into two primary matrices:
1. **The Natural/Religious Lexicon:** (e.g., *flood, tempest, divine water, hazard*)
2. **The Engineered/Commodified Lexicon:** (e.g., *water wheel, navigable canal, mill race, aqueduct*)

Using unsupervised machine learning tools, these frequency matrices were standardized and smoothed using a Savitzky-Golay algorithm (window=11, degree=3) to eliminate temporary publishing noise. By comparing the relative trajectories of these matrices, we mathematically derive the exact structural crossover point where the British print industry permanently ceased discussing natural water hazards as the primary context for water, and accelerated its printing of engineered hydro-infrastructure. The resulting structural crossover year ($T_0=1766$) serves as the precise historical treatment intervention. 

### 3.2 Econometric Merge (Difference-in-Differences)
To explicitly test the causal correlation between this cultural phenomenon and exponential geometric growth—the hallmark of macroeconomic modernity—the 1766 structural shift is overlaid onto real Historical GDP data from the Maddison Project Database (Dataverse, 2020 revision). 

We construct a multi-specification Difference-in-Differences (DiD) model treating Great Britain as the primary experimental group, using France and the Netherlands as contemporary 18th-century European controls. The model specifies both year and country fixed effects to eliminate unobserved cultural or baseline geographic variation. Serial autocorrelation, standard in multi-century economic datasets, is resolved via Newey-West HAC robust standard errors (autocovariance lag length=3). 

This methodology rigorously bounds the investigation. Pre-treatment parallel trends are explicitly validated using an interactive event-study matrix (5-year binning offsets relative to $T_0$), mathematically ensuring that the British geometric takeoff did not autonomously precede the hydro-social shift, but was strictly catalyzed concurrently with it. Finally, iterating the event study dates across the linguistic trajectories of *textiles*, *coal*, and *finance* establishes a placebo tournament, guaranteeing the integrity of water uniqueness.
