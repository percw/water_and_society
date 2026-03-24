# Reviewer 2: Transatlantic Corpus Contamination (Geographic Conflation)

## The Fatal Flaw

As Reviewer 2, holding PhDs in Quantitative Economic History and Computational Linguistics, I must point out a profound methodological catastrophe in this paper. The authors purport to correlate the linguistic commodification of water with the macroeconomic takeoff of the *British* Industrial Revolution. However, their primary linguistic data source—the generic `en-2019` Google Books Ngram corpus—is fundamentally misaligned with their macroeconomic variable.

The `en-2019` corpus represents an aggregation of English-language texts globally, predominantly driven by American and British publishing. Yet, the authors map this globally blended linguistic signal against *strictly British* (GBR) GDP per capita data from the Maddison Project.

This geographic conflation is fatal to the causal inference claimed. By the 19th century, the United States was industrializing on a vastly different resource and geographic scale, with a distinct trajectory of water technology (e.g., the massive Lowell mill system) and textual production. Thus, the observed "linguistic takeoff" in the `en-2019` corpus is severely contaminated by American publishing trends, rendering any supposed Granger causality between this transatlantic linguistic soup and *British* GDP statistically spurious and historically meaningless.

## Conclusion

The authors' failure to isolate British texts (e.g., using the `en-GB-2019` corpus) completely invalidates their central empirical claim. One cannot prove that linguistic shifts caused an economic takeoff in Britain using a dataset heavily diluted by the linguistic output of an entirely different, rapidly expanding continental economy. Until this geographic mismatch is resolved, the paper's core findings remain an artifact of poor data selection rather than a true reflection of the British hydro-social cycle.
