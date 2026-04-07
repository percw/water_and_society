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
- Mandatory replication policy → our GitHub repo is perfectly positioned
- Higher impact factor than Cliometrica

---

## Formatting Requirements

### Manuscript
- [ ] **Word count:** No strict stated limit, but main articles typically 8,000–12,000 words
- [ ] **Shorter papers:** 4,000–8,000 words (for replication studies, new methods, new data)
- [ ] **File type:** Word (.docx) or LaTeX
- [ ] **Citation style:** Author-date (verify against recent EEH articles)

### Front Matter
- [ ] **Abstract:** Required (typically 150–250 words)
- [ ] **Keywords:** Required
- [ ] **JEL classification codes:** Required
- [ ] **Title page:** Author information, affiliations, corresponding author

### Peer Review
- Check current policy — typically single-anonymous or double-anonymous
- Verify on Editorial Manager at submission time

### References
- Author-date in-text citations (e.g., "Crafts 1985")
- Full reference list at end
- Consistent format required

### Figures & Tables
- Electronic submission
- High resolution required
- EPS or TIFF preferred for production; PDF acceptable at submission
- Color figures free for online; check print policy

### ⚠️ MANDATORY Data & Replication Policy
- **All accepted papers MUST include:**
  - [ ] Full replication data files
  - [ ] Annotated program code
  - [ ] Command files (e.g., Python scripts with documentation)
  - [ ] Documentation sufficient for a third party to replicate all results
- Our GitHub repo (`percw/water_and_society`) satisfies this with:
  - `src/fetch_data.py` — data pipeline
  - `src/did_analysis.py` — full econometric pipeline
  - `requirements.txt` — dependency list
  - `data/` — generated outputs

---

## Our Current Gaps (Action Items)

| Item | Status | Action Needed |
|------|--------|---------------|
| Word count check | ❓ | Verify manuscript length |
| Abstract length | ❓ | May need slight trim or expansion |
| JEL codes | ❌ | Must add (see suggestions below) |
| Keywords | ❌ | Must add |
| Replication package | ✅ | GitHub repo already complete |
| Data Availability Statement | ✅ | Already in §8 |
| Cover letter | ❌ | Draft required |
| Competing interests | ❌ | Add declaration |

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
- Emphasize the full replication package
- Highlight transparent robustness reporting (HAC, clustered, collapsed DiD)
- Note placebo falsification tournaments as methodological rigor
- Frame as cliometric contribution that extends Crafts (1985) and Broadberry et al. (2015)
