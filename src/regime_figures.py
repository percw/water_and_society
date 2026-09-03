#!/usr/bin/env python3
"""
Publication figures for the regime / precondition analysis. Serif, 300 dpi, grayscale-safe
(line styles carry identity, colour is secondary). Writes data/fig_*.png.

Usage: python src/regime_figures.py   (run fetch_external.py, regime_analysis.py, mechanism_analysis.py first)
"""
from pathlib import Path
import numpy as np, pandas as pd, matplotlib as mpl, matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent; EXT = ROOT / 'data' / 'external'; OUT = ROOT / 'data'
mpl.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'Times', 'DejaVu Serif'], 'figure.dpi': 300, 'savefig.dpi': 300,
                     'axes.edgecolor': 'black', 'axes.linewidth': 0.8, 'axes.spines.top': False, 'axes.spines.right': False, 'font.size': 9,
                     'axes.titlesize': 10, 'axes.labelsize': 9, 'legend.fontsize': 8, 'legend.frameon': False})
C = {'k': '#111111', 'g': '#6d6d6d', 'l': '#b3b3b3', 'a': '#1f5f8b'}  # ink, grey, light, one accent
b = pd.read_csv(EXT / 'boe_gb.csv').set_index('Year'); b['GDPpc'] = b['GDP'] / b['PopGB']
cum = pd.read_csv(EXT / 'canal_cum_miles.csv', index_col=0).iloc[:, 0]; cum.index = cum.index.astype(int)
canals = pd.read_csv(EXT / 'uk_canals_wiki.csv'); panel = pd.read_csv(EXT / 'mpd_panel.csv')
w = np.exp(panel.pivot(index='year', columns='cc', values='lgdppc'))
irf = pd.read_csv(EXT / 'lp_irfs.csv'); sem = pd.read_csv(EXT / 'semantic_sequence.csv', index_col=0)
hp = pd.read_csv(EXT / 'power_hp.csv').set_index('Year')


def waves(ax):
    for a, e, lab in [(1760, 1780, 'first canal wave'), (1790, 1816, 'canal mania completions')]:
        ax.axvspan(a, e, color=C['l'], alpha=.35, lw=0); ax.text(a + 1, ax.get_ylim()[1], lab, fontsize=7, va='top', color=C['g'])


# Figure 1 — two growth regimes
fig, axs = plt.subplots(1, 2, figsize=(10, 4.2), sharex=True)
i = lambda s: s / s.loc[1700] * 100
for ax, series, title in [(axs[0], [('Total GDP', 'GDP', '-', C['k']), ('Population', 'PopGB', '--', C['g']), ('GDP per capita', 'GDPpc', ':', C['a'])], '(a) Aggregate and per-capita'),
                          (axs[1], [('Coal output', 'Coal', '-', C['k']), ('Industrial output', 'Ind', '--', C['g']), ('Agricultural output', 'Agri', ':', C['a'])], '(b) Sectors')]:
    for lab, col, ls, c in series: ax.plot(b.index, i(b[col]), ls, color=c, lw=1.4, label=lab)
    ax.set_yscale('log'); ax.set_ylim(60, 4000 if 'Sectors' in title else 1200); ax.set_xlim(1700, 1870)
    ax.set_yticks([100, 200, 400, 800, 1600, 3200] if 'Sectors' in title else [100, 200, 400, 800]); ax.get_yaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
    ax.axvline(1761, color=C['g'], lw=.8, ls='-.'); ax.axvline(1818, color=C['g'], lw=.8, ls='-.')
    ax.set_title(title, loc='left'); ax.set_ylabel('Index, 1700 = 100 (log scale)'); ax.legend(loc='upper left'); waves(ax)
axs[0].text(1762, 62, '1761', fontsize=7, color=C['g']); axs[0].text(1819, 62, '1818', fontsize=7, color=C['g'])
fig.suptitle('Figure 1. Britain\'s two growth regimes: aggregate output and population accelerate in the canal era, income per head only after 1818', x=0.01, ha='left', fontsize=10)
fig.tight_layout(); fig.savefig(OUT / 'fig1_two_regimes.png'); plt.close(fig)

# Figure 2 — canal dose and coal (three panels, no dual axis)
fig, axs = plt.subplots(1, 3, figsize=(11, 3.8))
dec = canals[(canals.year >= 1700) & (canals.year <= 1850)].groupby((canals.year // 10) * 10).miles.sum()
axs[0].bar(dec.index + 5, dec.values, width=8, color=C['g']); axs[0].set_title('(a) Canal miles opened per decade', loc='left'); axs[0].set_ylabel('Miles'); axs[0].set_xlim(1700, 1860)
axs[1].plot(cum.loc[1700:1850].index, cum.loc[1700:1850], color=C['k'], lw=1.6); axs[1].set_title('(b) Cumulative canal miles', loc='left'); axs[1].set_ylabel('Miles'); axs[1].set_xlim(1700, 1850)
cpc = (b['Coal'] / b['PopGB']); axs[2].plot(cpc.loc[1700:1850].index, cpc.loc[1700:1850] / cpc.loc[1700] * 100, color=C['a'], lw=1.4); axs[2].set_title('(c) Coal output per head, 1700 = 100', loc='left'); axs[2].set_xlim(1700, 1850)
lhp = np.log(hp.loc[1760:1870, ['steam_hp_k', 'water_hp_k', 'wind_hp_k']]).reindex(range(1760, 1871)).interpolate(method='index'); sh = np.exp(lhp['steam_hp_k']) / np.exp(lhp).sum(axis=1); xo = int(sh[sh >= .5].index.min())
axs[2].axvline(xo, color=C['g'], lw=.8, ls='-.'); axs[2].text(xo + 1, 120, f'steam > water + wind\npower, {xo}', fontsize=7, color=C['g'])
for ax in axs[1:]: waves(ax)
fig.suptitle('Figure 2. The canal network and coal: two waves of building; coal output per head doubles before steam is the majority power source', x=0.01, ha='left', fontsize=10)
fig.tight_layout(); fig.savefig(OUT / 'fig2_canal_dose.png'); plt.close(fig)

# Figure 3 — local projections
chains = [('canal→coal', 'Canal stock → coal output'), ('canal→steam hp', 'Canal stock → steam horsepower'), ('coal→steam hp', 'Coal output → steam horsepower'),
          ('canal→GDP per capita', 'Canal stock → GDP per capita'), ('steam hp→GDP per capita', 'Steam horsepower → GDP per capita'), ('canal→agriculture', 'Canal stock → agriculture (placebo)')]
fig, axs = plt.subplots(2, 3, figsize=(10, 5.6), sharex=True)
for ax, (key, title) in zip(axs.flat, chains):
    d = irf[irf.chain == key]; ax.fill_between(d.h, d.beta - 1.96 * d.se, d.beta + 1.96 * d.se, color=C['l'], alpha=.6, lw=0); ax.plot(d.h, d.beta, color=C['k'], lw=1.5)
    ax.axhline(0, color=C['g'], lw=.8); ax.set_title(title, loc='left'); ax.set_xlim(1, 20)
for ax in axs[1]: ax.set_xlabel('Horizon (years)')
for ax in axs[:, 0]: ax.set_ylabel('Cumulative log response')
fig.suptitle('Figure 3. Local projections along the precondition chain (95% HAC bands). Per 1,000 canal miles, or per log point of the regressor.', x=0.01, ha='left', fontsize=10)
fig.tight_layout(); fig.savefig(OUT / 'fig3_local_projections.png'); plt.close(fig)

# Figure 4 — war confound (single panel)
fig, ax = plt.subplots(figsize=(7.5, 4))
for c, lab, ls, col in [('GBR', 'Britain', '-', C['k']), ('FRA', 'France', '--', C['g']), ('NLD', 'Netherlands', ':', C['a'])]:
    s = w[c].loc[1780:1830] / w.loc[1790, c] * 100; ax.plot(s.index, s, ls, color=col, lw=1.5, label=lab)
ax.axvspan(1793, 1815, color=C['l'], alpha=.35, lw=0); ax.text(1794, 122, 'Revolutionary and Napoleonic Wars', fontsize=7, color=C['g']); ax.axvline(1807, color=C['g'], lw=.8, ls='-.')
ax.text(1807.5, 52, 'estimated break in the\nBritain–controls gap', fontsize=7, color=C['g'])
ax.set_ylim(50, 125); ax.set_ylabel('GDP per capita, 1790 = 100'); ax.legend(loc='lower left')
ax.set_title('Figure 4. The 1807 "break" in the cross-country design is the Dutch collapse', loc='left')
fig.tight_layout(); fig.savefig(OUT / 'fig4_war_confound.png'); plt.close(fig)

# Figure 5 — semantic sequencing
fig, ax = plt.subplots(figsize=(10, 4))
n = lambda s: (s.rolling(5, center=True).mean() / s.rolling(5, center=True).mean().loc[1850]) * 100
for col, lab, ls, c in [('canal', '“canal”', '-', C['k']), ('coal_by_water', 'coal-by-water bigrams (coal barge, coal wharf, coal boat, canal boat)', '--', C['a']), ('coal_by_steam', 'coal-by-steam bigrams (steam engine, steam power, steam boat)', ':', C['g'])]:
    s = n(sem[col]).loc[1740:1850]; ax.plot(s.index, s, ls, color=c, lw=1.5, label=lab)
ax.set_ylim(0, 130); ax.set_ylabel('Frequency, 1850 = 100 (5-year mean)'); ax.legend(loc='upper left'); ax.set_title('Figure 5. In print, coal travels by water before it is burned in engines (Google Books, British English)', loc='left')
fig.tight_layout(); fig.savefig(OUT / 'fig5_semantic_sequence.png'); plt.close(fig)

print('wrote', sorted(p.name for p in OUT.glob('fig*_*.png')))
