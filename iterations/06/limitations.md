# Iteration 06 — Limitations

## 18. Index Construction Fallacy (Domination by High-Frequency Unigrams)

**Critique:**
The composite indices constructed in Phase 1 (e.g., `hydro_mean` and `fossil_mean` seen in the Phase 1.3 macroeconomic overlay) are calculated using a simple arithmetic mean of raw Ngram frequencies across vocabulary lists. Because language follows a Zipfian distribution, highly frequent general terms completely mathematically dominate the composite index.

For instance, the raw frequency of the word "water" is orders of magnitude higher than specific, crucial technical terms like "pump" or "canal." By taking an unweighted mean of these frequencies, the resulting `hydro_mean` time series is functionally identical to the time series of the word "water" alone. The inclusion of the other technical words is mathematically irrelevant to the final Granger causality test results. The model is effectively just testing whether the word "water" Granger-causes GDP, completely failing to capture the *cluster* of industrial vocabulary it claims to represent.

## 19. Epistemological Overreach in Comparative Analysis (The Missing Multilingual Corpus)

**Critique:**
Phase 2.3 is explicitly titled "Comparative Analysis: Britain vs Asia" and concludes that the linguistic commodification of water is "a pattern absent in China and India." It uses the divergence in historical GDP between Britain, China, and India as a macroeconomic control variable to argue that the hydro-social shift was uniquely correlated with the British Industrial Revolution.

However, examining the data acquisition pipeline (`fetch_data.py`), the codebase *only* queries the `en-2019` English Google Books Ngram corpus. The pipeline analyzes absolutely zero Chinese or Indian textual data. To mathematically conclude the *absence* of a cultural or linguistic shift in a target culture without actually measuring that culture's texts is a massive logical and methodological failure. The current comparative analysis is comparing British economic divergence against Asian economic stagnation, but it is only providing one side of the linguistic equation.
