# Research Findings 01: The Hydro-Social Origins of the Industrial Revolution

## Executive Summary
This document presents the empirical findings from our econometric analysis testing the "water-first" hypothesis. The central question we investigate is whether Britain's early establishment of water and canal infrastructure acted as a primary catalyst and enabling condition for its industrial takeoff, *preceding* the widespread adoption of steam power.

The analysis indicates that a critical divergence in Britain's economic trajectory was initiated during the late 18th-century "Canal Era," establishing a foundation for the later "Steam Era."

---

## 1. Primary Evidence: Temporal Precedence

The timeline of linguistic shifts relative to economic divergence provides core support for the water-first hypothesis. We mapped the prevalence of vocabulary related to canal infrastructure alongside that of steam power, and compared both to the growing GDP gap between Britain and its continental peers (Netherlands and France).

![Figure 1: Canal Infrastructure Vocabulary Precedes and Predicts GDP Divergence](/Users/pcw/Documents/GitHub/Water_and_society/data/did_figure_one.png)

**Key Insight:** Canal vocabulary (green line) demonstrates a significant upward trend beginning around 1750, approximately **50 years before** steam-related vocabulary (red line) begins to rise. Notably, the widening GDP gap (dashed blue line) largely tracks the early rise of canal infrastructure, suggesting that economic divergence was underway before steam power became dominant.

---

## 2. Robustness Checks: Testing Alternative Narratives

To ensure the observed linguistic shift is not merely a general reflection of general progress or industrialization, we utilized a "Placebo Tournament" framework. This approach compared the predictive strength of our Water/Canal vocabulary against five prominent alternative historical narratives: Coal/Mining, Textiles, Finance, Agriculture, and Steam/Mechanics.

![Placebo Vocabulary Tournament](/Users/pcw/Documents/GitHub/Water_and_society/data/did_vocab_tournament.png)

**Key Insight:** Under a Difference-in-Differences (DiD) event study specification, **only the Water/Canal category maintained a consistent pattern.** 
A consistent result here requires no significant divergence *before* the vocabulary shifted (maintaining parallel trends), followed by an immediate sustained divergence *after*. The five alternative narratives displayed statistical noise prior to treatment and failed to align seamlessly with the structural break in GDP.

---

## 3. Quantifying Early Divergence (The Pre-Steam Era)

To evaluate the early impact of canal infrastructure, we examined what portion of Britain's ultimate economic lead was established prior to the widespread commercialization of steam. 

Measuring the GDP gap between Britain and its peers across milestones:
*   **1700 (Baseline):** Britain is slightly behind (-155 int'l $)
*   **1810 (End of the Canal Era):** Britain establishes a substantial lead (+1,150 int'l $)
*   **1900 (Peak of the Steam Era):** The lead grows further (+2,649 int'l $)

**Key Insight:** The data indicates that **47% of Britain's ultimate 1900 GDP lead was established by 1810.** A substantial economic shift had occurred prior to the point when steam power firmly dominated the industrial landscape.

---

## 4. Deconstructing the "Water Effect"

To analyze the specific mechanisms of early growth, we decomposed the water-related vocabulary into three distinct channels: Transport (canals/barges), Power (water wheels), and Manufacturing (mills).

![Channel Decomposition](/Users/pcw/Documents/GitHub/Water_and_society/data/did_channel_decomposition.png)

**Key Insight:** All three channels independently demonstrate highly significant, positive correlations with Britain's economic divergence. The shift encompassed transformations in transport logistics, energy harnessed, and localized manufacturing scale.

---

## Conclusion & Discussion

The econometric results suggest the following historical sequence:

1.  **Canals as Enabling Infrastructure:** The canal network integrated regional markets and reduced transport costs, creating the economic preconditions required for later mass production. This development originated in the mid-18th century.
2.  **Steam as the Accelerator:** As steam technology matured in the 19th century, it was deployed into an economy that had already been structurally integrated by earlier water network infrastructure.

While steam power became the heavily dominant force of the late 19th century—absorbing much of the statistical effect in models spanning the full 200-year window—the analysis highlights that **steam accelerated a broader industrial shift that water infrastructure had already initiated.**
