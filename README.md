# The Linguistic Hydro-Social Cycle

**Quantifying the First Mover Advantage of Water and its Macroeconomic Impact during the Industrial Revolution**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/percw/water_and_society/blob/main/hydro_social_analysis.ipynb)

## Overview

This project tests the hypothesis that the linguistic commodification of water preceded the semantic integration of fossil fuels (steam/coal) into the industrial vocabulary of 18th and 19th century Britain, and correlates this "First Mover" advantage with the macroeconomic takeoff of the Industrial Revolution.

## Methodology

The analysis is split into three computational phases:

1. **Topic Modeling (LDA)** — Tracks the transition of water's contextual usage from natural/religious to industrial over rolling 20-year time slices of the HathiTrust corpus.
2. **Diachronic Word Embeddings (Temporal Word2Vec)** — Trains decade-specific Word2Vec models to measure the semantic shift of "water", "steam", and "coal" relative to an industrial vocabulary cluster.
3. **Macroeconomic Overlay & Granger Causality** — Merges the NLP findings with Maddison Project GDP per capita data to test whether the hydro-linguistic shift preceded and Granger-caused the economic takeoff.

## Iterative Research Workflow

To ensure rigorous scientific development, this project uses a structured logging system in the `Iterations/` directory to document and address methodological challenges as they arise:
- **`XX.limitations.md`**: Captures critical scientific counter-arguments, corpus biases, or methodological weaknesses discovered during analysis (e.g., the lexical conflation of "steam mills" and "water mills").
- **`XX.addressing_limitations.md`**: Outlines the specific quantitative adjustments, data filters, or theoretical updates implemented to resolve the vulnerabilities raised in the corresponding limitations log.

## Quick Start

### Run Online (recommended)
Click the **"Open in Colab"** badge above — no local setup required. The notebook installs all dependencies automatically.

### Run Locally
```bash
git clone https://github.com/percw/water_and_society.git
cd water_and_society
pip install -r requirements.txt
jupyter notebook hydro_social_analysis.ipynb
```

## Data Sources

| Dataset | Description |
|---|---|
| **HathiTrust Extracted Features** | Volume-level metadata, token counts, and POS tagging (1700–1900) |
| **Google Books Ngram Corpus** | Frequency trajectories for engineering/technological vocabulary |
| **Maddison Project Database** | Historical GDP per capita for Britain, China, and India |

## Repository Structure

```
├── hydro_social_analysis.ipynb   # Main analysis notebook (Colab-ready)
├── hydro_social_analysis.py      # Equivalent Python script
├── Iterations/                   # Structured research logs (limitations & solutions)
├── research_proposal.md          # Full research proposal
├── requirements.txt              # Python dependencies
└── README.md
```

## License

This project is open source. See the research proposal for full academic context and methodology.
