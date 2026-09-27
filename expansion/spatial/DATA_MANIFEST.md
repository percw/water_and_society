# Data manifest for the spatial design

All of these exist. Most are free but need a registered download, and none of the hosts is reachable
from the cloud session that wrote this (only GitHub and PyPI are allowed there). Put each file in
`data/spatial/raw/` under the name given. `src/spatial/build_panel.py` (to be written once the formats
are seen) harmonises them into `data/spatial/parish_panel.csv`.

| # | Dataset | Needed for | Where | Access | Save as |
|---|---|---|---|---|---|
| 1 | **Navigable waterways of England and Wales, dynamic GIS 1600–1948** (Satchell, Newton and Shaw-Taylor 2017): polylines with opening and closing dates | Connection year for every unit (all three analyses) | Zenodo record 20122869 ("Navigable waterways for the UK 1600–1948"); CAMPOP transport datasets page; snapshots for 1820 and 1851 on ReShare (852997, 852998) | Zenodo files restricted (request access); ReShare free with registration | `waterways_dynamic.*` |
| 2 | **Wrigley–Schofield 404 parish register aggregates**, monthly baptisms, burials and marriages 1538–1837 | Analysis 1A (annual outcome) | UK Data Service, doi.org/10.5255/UKDA-SN-853082 | Free with registration | `ws404_aggregates.*` |
| 3 | **Parish populations 1801–1851** and **1851 parish boundary GIS** (CAMPOP, 12,641 quasi-parish units) | Analysis 1B; spatial units for everything | CAMPOP datasets page / UK Data Service | Free with registration | `parish_pop_1801_1851.*`, `parishes_1851.*` |
| 4 | **Exposed coalfields GIS** (Satchell and Shaw-Taylor 2013) | Analysis 2 moderator | CAMPOP GIS datasets; also in Bogart et al. historic urban dataset | Free / on request | `coalfields.*` |
| 5 | **Allen (2023) coal prices, 1695/1795/1842** | Analysis 2 mechanism | openICPSR project 193944 | Free with ICPSR login | `allen_coal_prices.*` |
| 6 | **Alvarez-Palau et al. (2025) replication package**: multimodal network 1680/1830, town costs | Robustness; market-access control | Zenodo record 14232197 | Open | `alvarez_palau_2025/` |
| 7 | **Early Engine Database** (c. 2,950 steam engines to 1800: year, location, use) | Analysis 3 | Association for Industrial Archaeology, industrial-archaeology.org/EarlyEngines | Full spreadsheet on application to the maintainers | `early_engines.xlsx` |
| 8 | **Elevation** (SRTM 90 m or OS Terrain 50) | Terrain instrument | OS Data Hub (open), OpenTopography | Open | `dem/` |
| 9 | **Priestley (1831) Acts** (already in repo) and never-built canals | Placebo treatment | `data/external/priestley_1831_acts.csv` | In repo | — |

## Hosts to allow for a cloud session to fetch the open ones itself

`zenodo.org`, `reshare.ukdataservice.ac.uk`, `beta.ukdataservice.ac.uk`, `www.campop.geog.cam.ac.uk`,
`www.openicpsr.org`, `osdatahub.os.uk`, `industrial-archaeology.org`, `sites.socsci.uci.edu`.
The registered downloads (2, 3, 5, 7, and the restricted Zenodo files in 1) have to be fetched by a
person with an account and committed or uploaded.

## Order of work

1. Fetch 1, 3, 4 first: they define units, treatment and moderator. Everything else hangs on them.
2. Build connection years; **before** attaching any outcome, report the cohort distribution and the
   number of treated and clean-control units per cohort (the power check).
3. Attach 2 and 3 (outcomes) and run analysis 1 exactly as registered.
4. Then 2 (complementarity), then 5, 7 (mechanism and steam), then the macro bridge.
