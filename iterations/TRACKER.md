# Iterations Tracker

Master log for tracking limitations and their resolution across iterations.

**Workflow:** Find limitations → log in `XX/limitations.md` → pick one → mark `in-progress` → implement solution → document in `XX/solutions.md` → mark `resolved`

## Status Legend

| Status | Meaning |
|--------|---------|
| `pending` | Identified, not yet addressed |
| `in-progress` | Actively being worked on |
| `resolved` | Solution implemented and documented |
| `revisited` | Previously resolved, reopened due to new findings |

## Tracker

| # | Limitation | Status | Solution Summary | Iteration |
|---|-----------|--------|-----------------|-----------|
| 1 | Fossil Capital critique — temporal precedence ≠ causal primacy | `resolved` | Bidirectional Granger: Hydro→GDP p=0.005, GDP→Hydro p=0.23 (reverse causation ruled out) | [01](01/) |
| 2 | Lexical conflation — early steam terms overlap with water terms | `resolved` | Unambiguous vocab (18 pure-hydro terms): Pure Hydro→GDP p=0.003 survives disambiguation | [01](01/) |
| 3 | Library bias — Ngram corpus skewed toward technical literature | `resolved` | OLS detrending against tech baseline: Detrended Hydro→GDP p=0.019 survives bias correction | [01](01/) |
