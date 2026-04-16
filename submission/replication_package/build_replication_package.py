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
    "src/did_analysis.py": "code/did_analysis.py",
    "src/dml_analysis.py": "code/dml_analysis.py",

    # Dependencies
    "requirements.txt": "requirements.txt",

    # Data outputs (CSV only — reproducible from scripts)
    "data/maddison_gdp.csv": "data/maddison_gdp.csv",
    "data/ngram_english.csv": "data/ngram_english.csv",

    # Figures (for reviewer reference)
    "data/did_figure_one.png": "figures/did_figure_one.png",
    "data/did_event_study.png": "figures/did_event_study.png",
    "data/did_vocab_tournament.png": "figures/did_vocab_tournament.png",
    "data/did_channel_decomposition.png": "figures/did_channel_decomposition.png",
    "data/did_parallel_trends.png": "figures/did_parallel_trends.png",
    "data/did_permutation_test.png": "figures/did_permutation_test.png",
    "data/did_regression_results.png": "figures/did_regression_results.png",
    "data/did_subperiod.png": "figures/did_subperiod.png",

    # Results log
    "docs/results.txt": "output/results.txt",

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
