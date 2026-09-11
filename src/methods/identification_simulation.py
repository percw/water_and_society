"""
Can a smooth, accumulating dose identify a sequence claim?

The paper's central inference is: the canal dose predicts coal and does NOT predict
income per head, therefore canals were a precondition rather than a rival cause.
That inference is only valid if the specification (i) has a correct rejection rate
under the null and (ii) would have detected a direct effect on income had one existed.

This Monte Carlo measures both, calibrated to the British series:
  n = 131 (1700-1830); dose R^2 on a quadratic trend = 0.976;
  residual sd and AR(1) taken from the paper's own quadratic-trend regressions.

Writes data/fig6_identification.png and prints the size-corrected thresholds.
"""
from pathlib import Path
import numpy as np, pandas as pd, matplotlib as mpl
import matplotlib.pyplot as plt, statsmodels.api as sm
from numpy.random import default_rng

ROOT = Path(__file__).resolve().parent.parent.parent
EXT, OUT = ROOT / 'data' / 'external', ROOT / 'data'
mpl.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'Times', 'DejaVu Serif'],
                     'figure.dpi': 300, 'savefig.dpi': 300, 'axes.edgecolor': 'black', 'axes.linewidth': 0.8,
                     'axes.spines.top': False, 'axes.spines.right': False, 'font.size': 9,
                     'axes.titlesize': 10, 'axes.labelsize': 9, 'legend.fontsize': 8, 'legend.frameon': False})
C = {'k': '#111111', 'g': '#6d6d6d', 'l': '#b3b3b3', 'a': '#1f5f8b'}

LO, HI = 1700, 1830
N = HI - LO + 1
t = np.arange(N, dtype=float)
war = np.isin(np.arange(LO, HI + 1),
              np.r_[np.arange(1756, 1764), np.arange(1775, 1784), np.arange(1793, 1816)]).astype(float)
TT = np.column_stack([np.ones(N), t, t ** 2, war])


def calibrate():
    """Effect sizes, trend growth, residual sd and AR(1) from the real series."""
    b = pd.read_csv(EXT / 'boe_gb.csv').set_index('Year')
    cum = pd.read_csv(EXT / 'canal_cum_miles.csv', index_col=0).iloc[:, 0]
    cum.index = cum.index.astype(int)
    yrs = np.arange(LO, HI + 1)
    D = cum.loc[yrs].values / 1000.0
    out = {'D': D}
    for nm, y in [('coal', b.loc[yrs, 'Coal'].values),
                  ('gdppc', (b.loc[yrs, 'GDP'] / b.loc[yrs, 'PopGB']).values)]:
        m = sm.OLS(np.log(y), np.column_stack([TT, D])).fit(cov_type='HAC', cov_kwds={'maxlags': 10})
        r = m.resid
        out[nm] = dict(beta=m.params[-1], p=m.pvalues[-1], sd=r.std(),
                       rho=sm.OLS(r[1:], r[:-1]).fit().params[0], g=m.params[1])
    q = np.polyval(np.polyfit(t, D, 2), t)
    out['trend_r2'] = 1 - ((D - q) ** 2).sum() / ((D - D.mean()) ** 2).sum()
    return out


def make_dose(rng, lumpiness, end):
    """A monotone accumulating stock shaped like the canal era, with controllable waves."""
    hump = np.exp(-0.5 * ((t - 0.62 * N) / (0.22 * N)) ** 2)
    if lumpiness > 0:
        wave = sum(np.sin(2 * np.pi * t / p + rng.uniform(0, 2 * np.pi))
                   for p in rng.uniform(25, 70, 3)) / 3
        hump = np.clip(hump * (1 + lumpiness * wave), 0, None)
    D = np.cumsum(hump)
    return D / D[-1] * end


def ar1(rng, rho, sd):
    e = rng.normal(0, sd * np.sqrt(1 - rho ** 2), N)
    u = np.empty(N); u[0] = rng.normal(0, sd)
    for i in range(1, N):
        u[i] = rho * u[i - 1] + e[i]
    return u


def dose_p(y, D):
    return sm.OLS(y, np.column_stack([TT, D])).fit(cov_type='HAC', cov_kwds={'maxlags': 10}).pvalues[-1]


def study(cal, reps=4000, seed=7):
    """Null distribution (size) and power curve for the income-per-head equation."""
    rng = default_rng(seed)
    end = cal['D'][-1]
    res = {}
    for nm in ('coal', 'gdppc'):
        c = cal[nm]
        ps = np.array([dose_p(4.6 + c['g'] * t + ar1(rng, c['rho'], c['sd']),
                              make_dose(rng, 1.0, end)) for _ in range(reps)])
        res[nm] = dict(size05=(ps < 0.05).mean(), size01=(ps < 0.01).mean(),
                       crit05=np.quantile(ps, 0.05), nulls=ps)
    c = cal['gdppc']
    gammas = np.array([0.0, 0.05, 0.10, 0.15, 0.20, 0.30])
    pw_c, pw_n = [], []
    for gm in gammas:
        ps = []
        for _ in range(1500):
            D = make_dose(rng, 1.0, end)
            ps.append(dose_p(4.6 + c['g'] * t + gm * D + ar1(rng, c['rho'], c['sd']), D))
        ps = np.array(ps)
        pw_c.append((ps < res['gdppc']['crit05']).mean()); pw_n.append((ps < 0.05).mean())
    res['power'] = dict(gammas=gammas, corrected=np.array(pw_c), nominal=np.array(pw_n), end=end)
    return res


def figure(cal, res):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4))

    grid = np.linspace(0.001, 0.10, 60)
    for nm, ls, col, lab in [('coal', '-', C['k'], 'coal equation'),
                             ('gdppc', '--', C['a'], 'income equation')]:
        actual = [(res[nm]['nulls'] < g).mean() for g in grid]
        a1.plot(grid, actual, ls, color=col, lw=1.6, label=lab)
    a1.plot([0, .10], [0, .10], ':', color=C['g'], lw=1.2, label='correctly sized')
    a1.axvline(0.05, color=C['l'], lw=0.8, zorder=0)
    a1.set_xlabel('nominal significance level'); a1.set_ylabel('actual rejection rate')
    a1.set_title('(a) The test rejects three to four times too often', loc='left')
    a1.set_xlim(0, .10); a1.set_ylim(0, .27); a1.legend(loc='upper left')

    p = res['power']
    eff = 100 * (np.exp(p['gammas'] * p['end']) - 1)
    a2.plot(eff, p['nominal'], '--', color=C['l'], marker='s', ms=4, label='nominal 5% (misleading)')
    a2.plot(eff, p['corrected'], '-', color=C['k'], marker='o', ms=4, label='size-corrected 5%')
    a2.axhline(.8, color=C['g'], ls=':', lw=1)
    a2.text(2, .82, '80% power', fontsize=7, color=C['g'])
    a2.set_xlabel('size of a direct effect on income by 1830, %')
    a2.set_ylabel('probability of detecting it')
    a2.set_title('(b) What the null on income can rule out', loc='left')
    a2.set_ylim(0, 1.02); a2.legend(loc='lower right')

    fig.tight_layout()
    fig.savefig(OUT / 'fig6_identification.png', bbox_inches='tight')
    print(f'  wrote {OUT / "fig6_identification.png"}')


if __name__ == '__main__':
    cal = calibrate()
    print(f"dose R2 on quadratic trend = {cal['trend_r2']:.4f}   n = {N}")
    print(f"  coal : beta={cal['coal']['beta']:+.3f}  p={cal['coal']['p']:.3f}  "
          f"sd={cal['coal']['sd']:.4f}  rho={cal['coal']['rho']:.3f}")
    print(f"  gdppc: beta={cal['gdppc']['beta']:+.3f}  p={cal['gdppc']['p']:.3f}  "
          f"sd={cal['gdppc']['sd']:.4f}  rho={cal['gdppc']['rho']:.3f}\n")
    res = study(cal)
    for nm in ('coal', 'gdppc'):
        r = res[nm]
        print(f"{nm:6s}  nominal 5% -> actual {r['size05']:.1%};  "
              f"nominal 1% -> actual {r['size01']:.1%};  "
              f"size-corrected 5% threshold p < {r['crit05']:.4f}")
    print()
    p = res['power']
    for gm, pc, pn in zip(p['gammas'], p['corrected'], p['nominal']):
        print(f"  gamma={gm:.2f} ({100*(np.exp(gm*p['end'])-1):4.0f}% by 1830): "
              f"power {pc:.1%} corrected, {pn:.1%} nominal")
    figure(cal, res)
