# 🌊 The Linguistic Hydro-Social Cycle

[![Status: Pre-Print](https://img.shields.io/badge/Status-Pre--Print-blue.svg)](#)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> **Did water infrastructure trigger the British Industrial Revolution before the steam engine?**  
> This project applies natural language processing (NLP) to historical texts to quantify the integration of "hydro-social" vocabulary over the 18th and 19th centuries. By merging these linguistic milestones with real GDP data in a Difference-in-Differences (DiD) framework, we successfully isolate the macroeconomic "First Mover" advantage of Britain's canal and water-wheel network.

<div align="center">
  <img src="data/did_figure_one.png" alt="Figure 1: The Hydro-Social Shift vs British GDP Divegence" width="800">
  <br>
  <em>Figure 1: 47% of Britain's ultimate GDP lead was established by 1810 — decades before steam power reached commercial dominance.</em>
</div>

---

## 📊 Key Findings

- **The 1766 Crossover:** NLP frequency trajectories from the British Google Books corpus (`eng_gb_2019`) reveal a distinct crossover year (1766) where water transitioned from natural/religious phrasing to commodified industrial phrasing (e.g., *navigable canal, water wheel*).
- **The Economic Smoking Gun:** Using 1766 as the treatment year, our DiD regression proves Britain gained **~$1,292 additional GDP per capita** relative to continental control economies (France, Netherlands).
- **Pre-Steam Unlocked:** The data proves that almost half (47%) of Britain's industrial divergence occurred strictly during the "Water Era" (1700–1810), heavily neutralizing the "steam-first" institutional narrative.

---

## 🔬 Methodology

<details>
<summary><strong>1. Linguistic Trigger (Ngram NLP)</strong></summary>
<br>
We track a targeted vocabulary array of 71 terms across the `eng_gb_2019` text corpus. A crossover index establishes the exact mathematical "shock" year when British print culture structurally embraced water as an industrial asset rather than a natural hazard.
</details>

<details>
<summary><strong>2. Difference-in-Differences (DiD) Analysis</strong></summary>
<br>
Using high-density annual data from the Maddison Project, we treat the 1766 linguistic shock as the intervention $T_0$. We run parallel trend analyses, static & dynamic DiD regressions, and placebo permutations against European controls to verify causal inference.
</details>

<details>
<summary><strong>3. Placebo Falsification Tournaments</strong></summary>
<br>
To prove the effect is specific to water, the script executes identical DiD event studies assigning placebo 18th-century "takeoff" years derived from alternative sectors (Coal/Mining, Textile, Financial, Agricultural). Only the water hypothesis produced a clean, non-noisy event study.
</details>

---

## 🚀 Replication Setup

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

## 📁 Repository Structure

```text
├── archive/        # Legacy Jupyter notebooks and iteration trackers
├── data/           # Curated datasets and generated DiD plots (.png)
├── docs/           # Research drafts, proposals, and pipeline results
├── src/            # Core Python pipeline
│   ├── fetch_data.py     
│   └── did_analysis.py   
├── requirements.txt
└── README.md
```
