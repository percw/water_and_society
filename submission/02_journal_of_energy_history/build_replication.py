#!/usr/bin/env python3
"""Assemble the anonymised replication archive for the energy-history submission.
Writes replication_package_anonymous.zip next to this script and fails if any file carries an identifying string."""
import re, zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent; ROOT = HERE.parent.parent
FILES = {
    'src/fetch_external.py': 'code/fetch_external.py', 'src/canal_series_v2.py': 'code/canal_series_v2.py',
    'src/regime_analysis.py': 'code/regime_analysis.py', 'src/mechanism_analysis.py': 'code/mechanism_analysis.py',
    'src/regime_figures.py': 'code/regime_figures.py',
    'src/methods/dose_identification.py': 'code/methods/dose_identification.py',
    'src/methods/identification_simulation.py': 'code/methods/identification_simulation.py',
    'src/methods/falsification.py': 'code/methods/falsification.py',
    'src/methods/falsification_figure.py': 'code/methods/falsification_figure.py',
    'requirements.txt': 'requirements.txt',
    'data/ngram_english.csv': 'data/ngram_english.csv',
    **{f'data/external/{f}': f'data/external/{f}' for f in [
        'boe_gb.csv', 'mpd_panel.csv', 'uk_canals_wiki.csv', 'canal_corrections.csv', 'uk_canals_v2.csv', 'canal_cum_miles.csv',
        'canal_cum_miles_v1.csv', 'priestley_1831_acts.csv', 'power_hp.csv', 'ngram_bigrams_coal_transport.csv', 'lp_irfs.csv',
        'semantic_sequence.csv', 'falsification_timing.csv', 'falsification_ri_quad.csv']},
    'data/fig1_two_regimes.png': 'figures/fig1_two_regimes.png', 'data/fig2_canal_dose.png': 'figures/fig2_canal_dose.png',
    'data/fig8_falsification.png': 'figures/fig3_falsification.png', 'data/fig4_semantic_sequence.png': 'figures/fig4_semantic_sequence.png',
    'docs/results_regime_v2.txt': 'output/results_regime.txt', 'docs/results_mechanism_v2.txt': 'output/results_mechanism.txt',
    'docs/results_falsification_v2.txt': 'output/results_falsification.txt',
    'docs/results_identification_v2.txt': 'output/results_identification.txt',
    'docs/results_regime_v1.txt': 'output/results_regime_v1_uncorrected.txt',
    'submission/02_journal_of_energy_history/REPLICATION_README.md': 'README.md',
}
BAD = re.compile(r'wessel|percw|github\.com/', re.I)
out = HERE / 'replication_package_anonymous.zip'
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for src, dst in FILES.items():
        p = ROOT / src; assert p.exists(), src
        if p.suffix in {'.py', '.md', '.txt', '.csv'}:
            assert not BAD.search(p.read_text(errors='ignore')), f'identifying string in {src}'
        z.write(p, f'replication/{dst}')
print(f'wrote {out.name}: {len(FILES)} files, {out.stat().st_size / 1024:.0f} KB')
