# Explorations in Economic History — Submission Requirements
> **Publisher:** Elsevier
> **ISSN:** 0014-4983
> **Portal:** https://www.sciencedirect.com/journal/explorations-in-economic-history
> **Submit via:** Elsevier Editorial Manager

---

## Why This Journal?

- Premier cliometrics journal — explicitly welcomes quantitative/formal approaches to any historical period
- Strong DiD tradition; reviewers will deeply engage with our econometric methodology
- Values honest robustness reporting (our transparent collapsed DiD discussion is an asset here)
- Mandatory replication policy → our GitHub repo + ZIP package is perfectly positioned
- Higher impact factor than Cliometrica

---

## Formatting Requirements

### Manuscript
- [x] **Word count:** No strict stated limit, but main articles typically 8,000–12,000 words — **Current: ~7,700 raw (~8,200 with footnotes/tables)**
- [ ] **Shorter papers:** 4,000–8,000 words (for replication studies, new methods, new data)
- [ ] **File type:** Word (.docx) or LaTeX — LaTeX compiled ✅, .docx conversion needed
- [x] **Citation style:** Author-date — **already used in manuscript ✅**

### Front Matter
- [x] **Abstract:** Required (typically 150–250 words) — **Current: 149 words** (at lower bound; may expand slightly for EEH)
- [x] **Keywords:** Required — see list below
- [x] **JEL classification codes:** Required — see list below
- [ ] **Title page:** Author information, affiliations, corresponding author

### Peer Review
- Check current policy — typically single-anonymous or double-anonymous
- Verify on Editorial Manager at submission time

### References
- [x] Author-date in-text citations (e.g., "Crafts 1985") — **already used ✅**
- [x] Full reference list at end — **24 references formatted ✅**
- [x] Consistent format required — standardized in §8

### Figures & Tables
- [x] Electronic submission — all figures in `data/` directory
- [x] High resolution required — 300 dpi, monochrome, generated via `format_plots_jeh.py`
- [ ] EPS or TIFF preferred for production; PDF acceptable at submission — PNG currently, may need conversion
- [x] Color figures free for online — using monochrome for print compatibility

### ⚠️ MANDATORY Data & Replication Policy
- **All accepted papers MUST include:**
  - [x] Full replication data files — `data/maddison_gdp.csv`, `data/ngram_english.csv`
  - [x] Annotated program code — `src/did_analysis.py`, `src/fetch_data.py`
  - [x] Command files (e.g., Python scripts with documentation) — full pipeline documented
  - [x] Documentation sufficient for a third party to replicate all results — `submission/replication_package/README.md`
- Our GitHub repo (`percw/water_and_society`) satisfies this with:
  - `src/fetch_data.py` — data pipeline
  - `src/did_analysis.py` — full econometric pipeline
  - `src/format_plots_jeh.py` — academic figure generation
  - `requirements.txt` — dependency list
  - `data/` — generated outputs
  - `submission/hydro_social_replication_20260407.zip` — self-contained replication archive (17 files)

---

## Current Gaps (Action Items)

| Item | Status | Action Needed |
|------|--------|---------------|
| Word count | ✅ | ~7,700 raw; within 8,000–12,000 range with footnotes |
| Abstract length | ⚠️ | 149 words — at lower boundary; consider expanding to ~180 for EEH |
| JEL codes | ✅ | Prepared (see below) |
| Keywords | ✅ | Prepared (see below) |
| Replication package | ✅ | GitHub repo + ZIP archive complete |
| Data Availability Statement | ✅ | Already in §8 |
| Title page | ❌ | Create with author details |
| Cover letter | ❌ | Draft required |
| Competing interests | ❌ | Add declaration |
| .docx conversion | ❌ | Convert if Editorial Manager requires Word |
| Figure format | ⚠️ | May need PNG → EPS/TIFF conversion for production |

---

## Suggested JEL Codes
- **N13** — Economic History: Europe (1913–)
- **N73** — Transport, International Trade, Energy: Europe (pre-1913)
- **O14** — Industrialization; Manufacturing and Service Industries
- **O33** — Technological Change: Choices and Consequences
- **C21** — Cross-Sectional Models; Spatial Models; Treatment Effect Models

## Suggested Keywords
1. Industrial Revolution
2. Difference-in-differences
3. Canal infrastructure
4. Economic divergence
5. Natural language processing
6. Water power

---

## Cover Letter Notes
- Lead with the methodological innovation: NLP + DiD = new evidence for a classic debate
- Emphasize the full replication package (mandatory compliance)
- Highlight transparent robustness reporting (HAC, clustered, collapsed DiD)
- Note placebo falsification tournaments as methodological rigor
- Frame as cliometric contribution that extends Crafts (1985) and Broadberry et al. (2015)
