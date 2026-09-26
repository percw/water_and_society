#!/usr/bin/env python3
"""Figure: what the canal dose can and cannot identify (timing placebo and randomisation inference).
Reads data/external/falsification_*.csv written by falsification.py. Writes data/fig8_falsification.png."""
from pathlib import Path
import numpy as np, pandas as pd, matplotlib as mpl, matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]; EXT = ROOT / 'data' / 'external'
mpl.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'Times', 'DejaVu Serif'], 'figure.dpi': 300, 'savefig.dpi': 300,
                     'axes.edgecolor': 'black', 'axes.linewidth': 0.8, 'axes.spines.top': False, 'axes.spines.right': False, 'font.size': 9,
                     'axes.titlesize': 10, 'axes.labelsize': 9, 'legend.fontsize': 8, 'legend.frameon': False})
C = {'k': '#111111', 'g': '#6d6d6d', 'l': '#b3b3b3', 'a': '#1f5f8b'}
tim = pd.read_csv(EXT / 'falsification_timing.csv'); ri = pd.read_csv(EXT / 'falsification_ri_quad.csv')

fig, axs = plt.subplots(1, 2, figsize=(10, 3.8))
ax = axs[0]
for c, lab, ls, col in [('Coal', 'Coal output', '-', C['k']), ('GDPpc', 'GDP per head', ':', C['a'])]:
    d = tim[tim.outcome == c]; ax.plot(d['shift'], d['t'], ls, marker='o', ms=3.5, color=col, lw=1.4, label=lab)
ax.axhline(3.0, color=C['g'], lw=.8, ls='--'); ax.axhline(0, color=C['l'], lw=.6); ax.axvline(0, color=C['l'], lw=.6)
ax.text(29, 3.1, 'size-corrected 5% bar', ha='right', va='bottom', fontsize=7, color=C['g'])
ax.text(-29, -2.1, '← leads: canals\n    not yet open', fontsize=7, color=C['g']); ax.text(29, -2.1, 'lags: canals →\nalready open', fontsize=7, color=C['g'], ha='right')
ax.set_xlabel('Shift of the canal stock (years)'); ax.set_ylabel('t-statistic on canal stock'); ax.set_xlim(-31, 31); ax.set_ylim(-2.5, 4.2)
ax.set_title('(a) Timing placebo, quadratic trend + war', loc='left'); ax.legend(loc='upper left')

ax = axs[1]
d = ri[(ri.outcome == 'Coal') & (ri['shift'] > 0)]; t0 = ri[(ri.outcome == 'Coal') & (ri['shift'] == 0)].t.iloc[0]
ax.hist(np.abs(d.t), bins=np.arange(0, 7.5, 0.5), color=C['l'], edgecolor='white', lw=1.5)
ax.axvline(abs(t0), color=C['k'], lw=1.6); ax.axvline(3.0, color=C['g'], lw=.8, ls='--')
p = (np.sum(np.abs(d.t) >= abs(t0)) + 1) / (len(d) + 1)
ax.annotate(f'actual canal stock\n|t| = {abs(t0):.1f}; RI p = {p:.2f}', xy=(abs(t0), 16), xytext=(4.4, 18), fontsize=7.5, va='center', arrowprops=dict(arrowstyle='-', color=C['k'], lw=.6))
ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(integer=True)); ax.set_ylim(0, 23)
ax.set_xlabel('|t| on canal stock, coal equation'); ax.set_ylabel('Placebo stocks (of 130)')
ax.set_title('(b) Randomisation inference: re-timed canal stocks', loc='left')
fig.tight_layout(); fig.savefig(ROOT / 'data' / 'fig8_falsification.png', bbox_inches='tight'); print('wrote data/fig8_falsification.png')
