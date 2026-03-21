Research Proposal
Title
The Linguistic Hydro-Social Cycle: Quantifying the First Mover Advantage of Water and its Macroeconomic Impact during the Industrial Revolution

1. Introduction & Background
The driving forces behind the Industrial Revolution and the subsequent "Great Divergence" between Europe and Asia remain highly debated. Prominent historians like Andreas Malm (Fossil Capital) and E.A. Wrigley emphasize coal and the steam engine as the primary catalysts for modern economic growth. In contrast, Terje Tvedt posits a hydro-centric narrative, arguing that England’s unique physical hydrology—and society's shifting relationship with it—was the true "first mover." Tvedt argues that the initial takeoff of the Industrial Revolution was fundamentally water-driven, and that fossil fuels merely capitalized on the economic and conceptual groundwork already laid by water infrastructure.

For this hydro-social transition to occur, society required a fundamental cultural shift in its perception of water—from a divine, untamable force of nature to an engineered, industrial commodity. While qualitative historical analyses have explored this shift, there remains a significant gap in large-scale empirical evidence. This project proposes a novel approach: utilizing Natural Language Processing (NLP) on massive digitized datasets to mathematically map this shifting perception, and overlaying this linguistic data against competing technologies (steam/coal) and historical GDP to test the "water-first" hypothesis.

2. Research Questions and Hypothesis
Primary Research Questions: 1. Can the conceptual shift of water—from a natural/religious element to a manageable industrial commodity—be empirically quantified in the historical text corpus of Britain between 1700 and 1900?
2. Did the linguistic commodification of water precede the linguistic prominence of fossil fuels (steam/coal), thereby validating the "water as first-mover" theory?
3. How does the trajectory of this hydro-social linguistic shift correlate with actual economic takeoff (GDP per capita) in Britain compared to non-industrializing regions like China and India?

Core Hypothesis: We hypothesize that the linguistic commodification of water in British texts was the leading indicator of the First Industrial Revolution, occurring decades before the linguistic rise of "steam" or "coal." Furthermore, we hypothesize that the trajectory of this hydro-social linguistic shift tightly correlates with the divergence in historical GDP per capita between Britain and Asia, whereas Asian texts from the same period will show a stagnant, agrarian/natural perception of water.

3. Data Sources
This research will rely on three highly structured, "plug-and-play" datasets:

HathiTrust Research Center (HTRC) Extracted Features Dataset: The core NLP dataset, providing volume-level metadata, token counts, and Part-of-Speech (POS) tagging for millions of public domain texts (1700–1900) across British, Chinese, and Indian contexts.

Google Books Ngram Corpus (English 1700–1900): A baseline dataset for analyzing the frequency trajectories of specific engineering and technological vocabulary.

The Maddison Project Database (2023 Update): A high-quality tabular dataset providing historical GDP per capita and population estimates for Britain, China, and India over the target centuries.

4. Methodology
The research will employ a three-phase computational methodology:

Phase 1: Topic Modeling (Latent Dirichlet Allocation - LDA)
Objective: To identify the emergence of "water as industry" as a distinct societal topic.

Process: We will run LDA over rolling 20-year time slices of the HathiTrust corpus to track the prominence of topics containing keywords like river, mill, engineer, pump, canal. We will plot the chronological rise of "industrial water" topics against the decline of "agrarian/natural water" topics.

Phase 2: Diachronic Word Embeddings (Temporal Word2Vec)
Objective: To measure the semantic shift of the word "water" and compare it to competing technologies.

Process: We will train Word2Vec models on sequential decades of the text corpus. We will calculate the cosine similarity between the vector for "water" and target vectors for industrialization (e.g., "machine," "power," "capital").

The "First Mover" Test: We will simultaneously track the semantic clusters for "steam," "coal," and "fossil fuels." We will mathematically measure the temporal lag between water's integration into the "industry" semantic space versus steam's integration into that same space.

Phase 3: Macroeconomic Overlay and Causal Testing
Objective: To link cultural/linguistic shifts to actual economic growth.

Process: We will extract the vector distances and topic frequencies from Phases 1 and 2 and plot them on a unified timeline against historical GDP per capita from the Maddison Project.

Measurement: We will conduct time-series correlation analysis (including Granger causality tests) to determine if the hydro-linguistic shift preceded or coincided with the economic "hockey stick" of the British Industrial Revolution, and demonstrate the absence of both in the Asian control datasets.

5. Expected Contributions & Outcomes
Direct Engagement with the Fossil Capital Debate: By mapping competing technologies on the same timeline, this project will use mathematical data to test whether fossil capital was the driver of the Industrial Revolution, or a latecomer that piggybacked on water.

Empirical Validation of Tvedt's Theories: This project moves the hydro-social theories of Terje Tvedt from qualitative historical debate into data-driven cliometrics.

Open Source Deliverables: The project will produce an open-source Python repository containing the data-cleaning pipelines, trained historical word embeddings, and interactive visualizations mapping the semantic shift of water against historical GDP.

6. Proposed Timeline
Month 1: Data Acquisition. Querying the HathiTrust API, downloading Extracted Features, and structuring the Maddison GDP data.

Month 2: Baseline NLP. Running Ngram frequency analyses, basic token-counting, and initial LDA topic modeling.

Month 3: Word Embeddings. Training Temporal Word2Vec models to calculate cosine similarities across time slices for "water," "steam," and "coal."

Month 4: Macroeconomic Integration. Overlaying NLP metrics with Maddison GDP data and running time-series correlation/Granger causality tests.

Month 5: Comparative Analysis. Contrasting the British linguistic and economic data with the available corpora for China/India.

Month 6: Synthesis & Publication. Drafting the final paper, finalizing data visualizations, and publishing the open-source code repository.