#!/usr/bin/env python3
"""
build_replication_package.py — Assembles a distributable replication archive.

Creates a self-contained ZIP file containing all code, data, and documentation
necessary for third-party replication, as required by journal data policies.

Usage:
    python build_replication_package.py
"""

import shutil
import zipfile
from pathlib import Path
from datetime import datetime

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
PACKAGE_DIR = PROJECT_DIR / "submission" / "replication_package"
OUTPUT_DIR = PROJECT_DIR / "submission"

# Files to include in the replication package
INCLUDE_FILES = {
    # Core scripts
    "src/fetch_data.py": "code/fetch_data.py",
    "src/fetch_external.py": "code/fetch_external.py",
    "src/regime_analysis.py": "code/regime_analysis.py",
    "src/mechanism_analysis.py": "code/mechanism_analysis.py",
    "src/regime_figures.py": "code/regime_figures.py",
    "src/did_analysis.py": "code/did_analysis.py",
    "src/dml_analysis.py": "code/dml_analysis.py",

    # Dependencies
    "requirements.txt": "requirements.txt",

    # Data (tidy CSVs; raw downloads regenerate via fetch_external.py)
    "data/maddison_real_gdp.csv": "data/maddison_real_gdp.csv",
    "data/ngram_english.csv": "data/ngram_english.csv",
    "data/external/boe_gb.csv": "data/external/boe_gb.csv",
    "data/external/mpd_panel.csv": "data/external/mpd_panel.csv",
    "data/external/uk_canals_wiki.csv": "data/external/uk_canals_wiki.csv",
    "data/external/canal_cum_miles.csv": "data/external/canal_cum_miles.csv",
    "data/external/priestley_1831_acts.csv": "data/external/priestley_1831_acts.csv",
    "data/external/power_hp.csv": "data/external/power_hp.csv",
    "data/external/ngram_bigrams_coal_transport.csv": "data/external/ngram_bigrams_coal_transport.csv",
    "data/external/lp_irfs.csv": "data/external/lp_irfs.csv",
    "data/external/semantic_sequence.csv": "data/external/semantic_sequence.csv",

    # Figures
    "data/fig1_two_regimes.png": "figures/fig1_two_regimes.png",
    "data/fig2_canal_dose.png": "figures/fig2_canal_dose.png",
    "data/fig3_local_projections.png": "figures/fig3_local_projections.png",
    "data/fig4_war_confound.png": "figures/fig4_war_confound.png",
    "data/fig5_semantic_sequence.png": "figures/fig5_semantic_sequence.png",
    "data/fig6_power_benchmark.png": "figures/fig6_power_benchmark.png",
    "data/did_event_study.png": "figures/earlier_version_did_event_study.png",

    # Results logs
    "docs/results_regime_v1.txt": "output/results_regime_v1.txt",
    "docs/results_mechanism_v1.txt": "output/results_mechanism_v1.txt",
    "docs/results_v5.txt": "output/results_earlier_version_did.txt",

    # Manuscript
    "archive/paper/compiled_manuscript.md": "manuscript/compiled_manuscript.md",
    "archive/paper/compiled_manuscript.tex": "manuscript/compiled_manuscript.tex",

    # Replication instructions
    "submission/replication_package/README.md": "README.md",
}


def build_package():
    timestamp = datetime.now().strftime("%Y%m%d")
    zip_name = f"hydro_social_replication_{timestamp}.zip"
    zip_path = OUTPUT_DIR / zip_name

    print(f"Building replication package: {zip_name}")
    print(f"{'='*60}")

    included = 0
    skipped = []

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for src_rel, dst_rel in sorted(INCLUDE_FILES.items()):
            src_path = PROJECT_DIR / src_rel
            if src_path.exists():
                zf.write(src_path, f"replication/{dst_rel}")
                size_kb = src_path.stat().st_size / 1024
                print(f"  ✅ {dst_rel:<55} ({size_kb:.1f} KB)")
                included += 1
            else:
                skipped.append(src_rel)
                print(f"  ⚠️  MISSING: {src_rel}")

    # Report
    print(f"\n{'='*60}")
    print(f"📦 Package: {zip_path}")
    print(f"   Files included: {included}/{len(INCLUDE_FILES)}")
    if skipped:
        print(f"   ⚠️  Skipped {len(skipped)} missing files:")
        for s in skipped:
            print(f"      - {s}")
    print(f"   Size: {zip_path.stat().st_size / 1024:.1f} KB")
    print(f"{'='*60}")

    return zip_path


if __name__ == '__main__':
    build_package()
