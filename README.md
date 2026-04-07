# The Linguistic Hydro-Social Cycle

[![Status: Pre-Print](https://img.shields.io/badge/Status-Pre--Print-blue.svg)](#)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

📖 **[Read the Full Pre-Print Manuscript Draft Here](archive/paper/compiled_manuscript.md)**

> **Did water infrastructure establish the preconditions for British industrialization — decades before the steam engine?**
> This project applies natural language processing (NLP) to historical texts to quantify the integration of "hydro-social" vocabulary over the 18th and 19th centuries. By merging these linguistic milestones with real GDP data in a Difference-in-Differences (DiD) framework, we trace the origins of Britain's macroeconomic divergence to the canal era — establishing that water infrastructure functioned as a necessary precondition for the fossil transition that followed.

<div align="center">
  <img src="data/did_figure_one.png" alt="Figure 1: The Hydro-Social Shift vs British GDP Divergence" width="800">
  <br>
  <em>Figure 1: 47% of Britain's ultimate GDP lead was established by 1810 — decades before steam power reached commercial dominance.</em>
</div>

---

## The Great Divergence in Infrastructure

Britain's industrial trajectory was not simply a story of coal and steam. Before the first commercially viable steam engines, Britain had already engineered a national network of navigable canals, towpaths, and water-powered mills — cooperating with the landscape rather than overriding it. This "geographical symbiosis" created the integrated markets, accumulated capital, and systemic demand that the subsequent fossil revolution would build upon.

The contrast with contemporary Asian river transport illustrates why Britain's specific hydro-topographical engineering mattered. While Chinese river systems were vast, they lacked the engineered infrastructure — towpaths, locks, low-profile barges — that made British canals uniquely efficient for bulk industrial transport.

<table>
<tr>
<td width="50%">

<div align="center">
  <img src="data/illustrations/England_River.png" alt="English Canal Infrastructure, c. 1743" width="100%">
  <br>
  <em><strong>English Canal Infrastructure, c. 1743.</strong> Observed loading at Loxley Quay. Note the engineered towpath, horse-drawn traction, low-profile barge ("The Industry") designed for bridge clearance, crane-assisted loading, and the integrated water wheel powering adjacent mills. A single horse replaces dozens of labourers.</em>
</div>

</td>
<td width="50%">

<div align="center">
  <img src="data/illustrations/Asia_River.png" alt="Asian River Transport, Three Gorges, c. 1750" width="100%">
  <br>
  <em><strong>Asian River Transport, Three Gorges, c. 1750.</strong> In stark contrast: no continuous towpath, no horse traction, no engineered profile. Massive crews haul wide-hulled junks by brute force through fast current. The sheer difficulty of transport without topographical engineering magnified costs and constrained market integration.</em>
</div>

</td>
</tr>
</table>

This infrastructural contrast sits at the heart of the ["Great Divergence"](https://en.wikipedia.org/wiki/Great_Divergence) debate (Pomeranz 2000; Tvedt 2010). Britain's advantage was not merely geological (coal) or cultural (rhetoric) — it was *topographical*: a landscape uniquely amenable to engineered water cooperation, systematically exploited through canal construction from 1761 onward.

---

## Key Findings

- **The 1761 Structural Break:** The opening of the Bridgewater Canal serves as the exogenous treatment shock ($T_0$). The 1766 NLP crossover in the Google Books `eng_gb_2019` corpus — where water terminology permanently shifts from naturalistic to engineered — validates the mechanism five years later.
- **The Treatment Effect:** DiD regression yields $\beta_3 = 1{,}251$ additional GDP per capita for Britain relative to continental controls ($p = 0.042$, HAC). The point estimate is robust across all variance corrections, including the collapsed estimator of Bertrand et al. (2004).
- **The Precondition Thesis:** 47% of Britain's ultimate industrial divergence was established by 1810 — during the canal and water wheel era. When fossil and transport channels are entered simultaneously, the fossil channel dominates — consistent with water infrastructure's contribution being absorbed into the broader economic structure it created.
- **Falsification:** Only the water infrastructure shock produces a clean event study. Rival vocabularies (coal, textiles, finance) yield noisy or invalid pre-trends.

---

## Methodology

<details>
<summary><strong>1. Linguistic Trigger (Ngram NLP)</strong></summary>
<br>
We track a targeted vocabulary array of 71 terms across the <code>eng_gb_2019</code> text corpus. A crossover index establishes the exact mathematical "shock" year when British print culture structurally embraced water as an industrial asset rather than a natural hazard.
</details>

<details>
<summary><strong>2. Difference-in-Differences (DiD) Analysis</strong></summary>
<br>
Using high-density annual data from the Maddison Project, we deploy the 1761 Bridgewater Canal opening as the exogenous treatment $T_0$. We run parallel trend analyses, static & dynamic DiD regressions, HAC/clustered/collapsed robustness checks, and placebo permutations against European controls.
</details>

<details>
<summary><strong>3. Placebo Falsification Tournaments</strong></summary>
<br>
To demonstrate specificity, the script executes identical DiD event studies assigning placebo 18th-century "takeoff" years derived from alternative sectors (Coal/Mining, Textile, Financial, Agricultural). Only the water hypothesis produced a clean, non-noisy event study aligned with the timing of GDP divergence.
</details>

---

## Replication Setup

To reproduce the data fetching and exact econometric graphs for publication:

```bash
# 1. Clone the repository
git clone https://github.com/percw/water_and_society.git
cd water_and_society

# 2. Setup virtual environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Pull linguistic data and regenerate causal plots
python src/fetch_data.py --force
python src/did_analysis.py
```

## Repository Structure

```text
├── archive/              # Paper sections (Markdown + compiled LaTeX)
│   └── paper/
│       ├── 00_abstract.md ... 08_references.md
│       ├── compiled_manuscript.md
│       └── compiled_manuscript.tex
├── data/                 # Datasets, generated plots, and illustrations
│   ├── illustrations/    # Historical canal infrastructure comparisons
│   ├── did_figure_one.png
│   ├── did_event_study.png
│   └── ...
├── docs/                 # Research results and pipeline outputs
├── src/                  # Core Python pipeline
│   ├── fetch_data.py
│   └── did_analysis.py
├── requirements.txt
└── README.md
```
