"""
The boundary condition: how big must an effect be before this design can see it,
as a function of how trend-like the dose is?

For each of a range of dose paths, we measure
  - the actual rejection rate of a nominal 5% test under the null (size)
  - the size-corrected 5% threshold
  - the minimum effect detectable with 80% power at that corrected threshold (MDE)

and plot MDE against the dose's R^2 on a quadratic trend. Britain's canal dose
sits at 0.976; the Priestley authorisation dose at 0.982.

Writes data/fig7_boundary.png and data/external/boundary_sweep.csv.
"""
from pathlib import Path
import numpy as np, pandas as pd, matplotlib as mpl
import matplotlib.pyplot as plt
from numpy.random import default_rng
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from dose_identification import Noise, Design, trend_r2, burst_dose

ROOT = Path(__file__).resolve().parent.parent.parent
OUT, EXT = ROOT / 'data', ROOT / 'data' / 'external'
mpl.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'Times', 'DejaVu Serif'],
                     'figure.dpi': 300, 'savefig.dpi': 300, 'axes.edgecolor': 'black', 'axes.linewidth': 0.8,
                     'axes.spines.top': False, 'axes.spines.right': False, 'font.size': 9,
                     'axes.titlesize': 10, 'axes.labelsize': 9, 'legend.fontsize': 8, 'legend.frameon': False})
C = {'k': '#111111', 'g': '#6d6d6d', 'l': '#b3b3b3', 'a': '#1f5f8b'}

N, DOSE_END = 131, 2.32
INCOME = Noise(sd=0.0411, rho=0.395, growth=0.00202)     # calibrated to GB income per head
WAR = np.isin(np.arange(1700, 1700 + N),
              np.r_[np.arange(1756, 1764), np.arange(1775, 1784), np.arange(1793, 1816)]).astype(float)
SIZE_REPS, POWER_REPS = 1200, 500


def mde(design, threshold, target=0.80, lo=0.01, hi=0.80, steps=8, seed=1):
    """Smallest gamma detectable with `target` power, by bisection."""
    for i in range(steps):
        mid = (lo + hi) / 2
        if design.power(mid, threshold, reps=POWER_REPS, seed=seed + i) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main():
    rng = default_rng(42)
    rows = []
    plan = [(k, reps) for k, reps in
            [(1, 4), (2, 4), (3, 4), (4, 4), (6, 4), (10, 4), (20, 3), (40, 3)]]
    for k, reps in plan:
        for j in range(reps):
            D = burst_dose(rng, N, k, end=DOSE_END)
            r2 = trend_r2(D)
            d = Design(dose=D, noise=INCOME, controls=WAR)
            size, crit = d.size(reps=SIZE_REPS, seed=int(r2 * 1e6) % 99991)
            g = mde(d, crit, seed=7 + j)
            pct = 100 * (np.exp(g * DOSE_END) - 1)
            rows.append(dict(bursts=k, trend_r2=r2, size05=size, crit05=crit,
                             mde_gamma=g, mde_pct=pct))
            print(f'  bursts={k:3d}  R2={r2:.4f}  size={size:5.1%}  '
                  f'corrected p<{crit:.4f}  MDE={pct:5.1f}% by end', flush=True)
    df = pd.DataFrame(rows).sort_values('trend_r2')
    df.to_csv(EXT / 'boundary_sweep.csv', index=False)
    figure(df)
    return df


def figure(df):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4))
    x = df.trend_r2.values

    a1.scatter(x, df.size05, s=16, color=C['k'], zorder=3)
    a1.axhline(0.05, color=C['g'], ls=':', lw=1.2)
    a1.set_ylim(0, 0.23)
    a1.text(0.862, 0.058, 'a correctly sized test would sit here', fontsize=7, color=C['g'])
    for v, lab, ls in [(0.9760, 'canal miles', '-'), (0.9819, 'Priestley acts', '--')]:
        a1.axvline(v, color=C['a'], ls=ls, lw=1)
    a1.text(0.9735, 0.215, 'Britain', fontsize=7, color=C['a'], ha='right')
    a1.set_xlabel('dose $R^2$ on a quadratic trend')
    a1.set_ylabel('actual rejection rate of a nominal 5% test')
    a1.set_title('(a) The test over-rejects by the same margin whatever the dose', loc='left')

    a2.scatter(x, df.mde_pct, s=16, color=C['k'], zorder=3)
    for v, ls in [(0.9760, '-'), (0.9819, '--')]:
        a2.axvline(v, color=C['a'], ls=ls, lw=1)
    a2.text(0.9735, a2.get_ylim()[1]*0.93, 'Britain', fontsize=7, color=C['a'], ha='right')
    a2.set_xlabel('dose $R^2$ on a quadratic trend')
    a2.set_ylabel('smallest effect detectable with 80% power, %')
    a2.set_title('(b) But it goes blind as the dose becomes a trend', loc='left')

    fig.tight_layout()
    fig.savefig(OUT / 'fig7_boundary.png', bbox_inches='tight')
    print(f'\nwrote {OUT / "fig7_boundary.png"}')


if __name__ == '__main__':
    main()
