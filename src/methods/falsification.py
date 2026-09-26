#!/usr/bin/env python3
"""
Falsification tests a referee would run on the canal-dose result.

  A. Timing placebo.  Coal on the canal stock shifted by s years, quadratic trend
     + war dummy, 1700-1830.  A precondition predicts that the stock of canals
     already open (lags, s > 0) predicts coal better than canals not yet open
     (leads, s < 0).  If leads predict as well as lags, the dose is proxying the
     trend and the sequencing claim fails.
  B. Randomisation inference on the first-difference specification.  The annual
     series of new mileage is circularly shifted within 1700-1830 (130 placebo
     orderings that keep its lumpiness and autocorrelation) and the ten-lag sum is
     re-estimated.  The RI p-value does not rely on HAC standard errors, which
     src/methods/ shows are oversized on this sample.
  C. The same randomisation for the ten-year local projection.
  D. Joint F versus cumulative sum in the first-difference model.
  E. Randomisation inference for the quadratic-trend specification.

Usage:  python src/methods/falsification.py | tee docs/results_falsification_v1.txt
"""
import warnings; warnings.filterwarnings('ignore')
from pathlib import Path
import numpy as np, pandas as pd, statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[2]
EXT = ROOT / 'data' / 'external'
HAC = dict(cov_type='HAC', cov_kwds={'maxlags': 10})

b = pd.read_csv(EXT / 'boe_gb.csv').set_index('Year'); b['GDPpc'] = b['GDP'] / b['PopGB']
lg = np.log(b)
cum = pd.read_csv(EXT / 'canal_cum_miles.csv', index_col=0).iloc[:, 0]; cum.index = cum.index.astype(int)
cum = (cum / 1000).reindex(range(1650, 1901)).ffill().fillna(0.0)
war = pd.Series(0, index=range(1700, 1901)); war.loc[1756:1763] = 1; war.loc[1775:1783] = 1; war.loc[1793:1815] = 1
A, E = 1700, 1830
OUT = ['Coal', 'Ind', 'PopGB', 'GDP', 'GDPpc', 'Agri']


def quad(c, dose):
    y = lg[c].loc[A:E]; t = y.index.values.astype(float) - A
    X = sm.add_constant(pd.DataFrame({'t': t, 't2': t ** 2 / 1000, 'war': war.loc[A:E].values,
                                      'dose': dose.reindex(y.index).values}, index=y.index))
    r = sm.OLS(y, X).fit(**HAC); return r.params['dose'], r.tvalues['dose']


def fd_sum(c, new):
    dy = lg[c].diff(); Z = pd.concat([new.shift(k).rename(f'l{k}') for k in range(11)], axis=1)
    d = pd.concat([dy.rename('dy'), Z], axis=1).loc[A + 11:E].dropna()
    r = sm.OLS(d['dy'], sm.add_constant(d.drop(columns='dy'))).fit()
    w = np.r_[0, np.ones(11)]; return float(w @ r.params.values), float((w @ r.params.values) / np.sqrt(w @ r.cov_params().values @ w))


def lp10(c, dose, h=10):
    y = lg[c]; d = pd.concat([(y.shift(-h) - y).rename('dy'), dose.rename('x'), y.rename('y0')], axis=1)
    d['t'] = d.index.astype(float); d = d.loc[A:E - h].dropna()
    r = sm.OLS(d['dy'], sm.add_constant(d[['x', 'y0', 't']])).fit(); return r.params['x'], r.tvalues['x']


print('=' * 78 + '\nA. TIMING PLACEBO: log y ~ quadratic trend + war + canal stock shifted s years, 1700-1830\n'
      '   s > 0: stock s years earlier (lag); s < 0: stock s years later (lead, canals not yet open)\n' + '=' * 78)
shifts = list(range(-30, 31, 5))
rows = []
for c in OUT:
    for s in shifts:
        bb, tt = quad(c, cum.shift(s)); rows.append((c, s, bb, tt))
tab = pd.DataFrame(rows, columns=['outcome', 'shift', 'coef', 't'])
print(tab.pivot(index='shift', columns='outcome', values='t')[OUT].round(2).to_string())
print('(t-statistics, Newey-West 10 lags; size-corrected 5% critical value is about |t| > 3.0)')

new = cum.diff().loc[A:E]
print('\n' + '=' * 78 + '\nB. RANDOMISATION INFERENCE, first differences, 10-lag cumulative response\n'
      '   placebo = new-mileage series circularly shifted within 1700-1830 (130 orderings)\n' + '=' * 78)
n = len(new)
for c in OUT:
    b0, t0 = fd_sum(c, cum.diff())
    ts = []
    for k in range(1, n):
        p = pd.Series(np.roll(new.values, k), index=new.index).reindex(cum.index).fillna(0.0)
        ts.append(fd_sum(c, p)[1])
    ts = np.array(ts); ri = (np.sum(np.abs(ts) >= abs(t0)) + 1) / (len(ts) + 1)
    print(f'  {c:6s}: sum {100*b0:+6.1f}% per 1,000 miles, t={t0:+.2f}, RI p={ri:.3f}  (placebo |t| 95th pct {np.percentile(np.abs(ts), 95):.2f})')

print('\n' + '=' * 78 + '\nC. RANDOMISATION INFERENCE, local projection h=10 (level + trend controls)\n'
      '   placebo = canal stock rebuilt from the circularly shifted new-mileage series\n' + '=' * 78)
for c in OUT:
    b0, t0 = lp10(c, cum)
    ts = []
    for k in range(1, n):
        p = pd.Series(np.roll(new.values, k), index=new.index).cumsum().reindex(cum.index).ffill().fillna(0.0)
        ts.append(lp10(c, p)[1])
    ts = np.array(ts); ri = (np.sum(np.abs(ts) >= abs(t0)) + 1) / (len(ts) + 1)
    print(f'  {c:6s}: {100*b0:+6.1f}% per 1,000 miles at 10 years, t={t0:+.2f}, RI p={ri:.3f}')

print('\n' + '=' * 78 + '\nD. WHAT TABLE 3 REPORTS FOR FIRST DIFFERENCES: joint F of 11 lags vs the cumulative sum\n'
      '   A significant joint F says the lags are not all zero; it does not say their sum is positive.\n' + '=' * 78)
for c in OUT:
    dy = lg[c].diff(); Z = pd.concat([cum.diff().shift(k).rename(f'l{k}') for k in range(11)], axis=1)
    d = pd.concat([dy.rename('dy'), Z], axis=1).loc[A + 11:E].dropna()
    r = sm.OLS(d['dy'], sm.add_constant(d.drop(columns='dy'))).fit(**HAC)
    w = np.r_[0, np.ones(11)]; s = w @ r.params.values; se = np.sqrt(w @ r.cov_params().values @ w)
    from scipy import stats as _st; print(f'  {c:6s}: sum {100*s:+6.1f}%  HAC t(sum)={s/se:+.2f} p(sum)={2*_st.norm.sf(abs(s/se)):.3f}  joint F p={float(r.f_test(np.eye(11, 12, 1)).pvalue):.4f}')

print('\n' + '=' * 78 + '\nE. RANDOMISATION INFERENCE, quadratic trend + war (Table 3, column 2)\n' + '=' * 78)
for c in OUT:
    b0, t0 = quad(c, cum); ts = []
    for k in range(1, n):
        p = pd.Series(np.roll(new.values, k), index=new.index).cumsum().reindex(cum.index).ffill().fillna(0.0)
        ts.append(quad(c, p)[1])
    ts = np.abs(np.array(ts)); ri = (np.sum(ts >= abs(t0)) + 1) / (len(ts) + 1)
    print(f'  {c:6s}: {100*b0:+6.1f}% per 1,000 miles, t={t0:+.2f}, RI p={ri:.3f}')
