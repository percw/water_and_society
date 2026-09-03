#!/usr/bin/env python3
"""
Regime analysis: canals as a precondition for coal-based industrialisation.

Reproduces every number in docs/memos/2026-09-03_canals_before_steam.html.
Requires data/external/*.csv (run src/fetch_external.py first).

Sections
  1. War confound in the cross-country DiD (Maddison 2023)
  2. Britain's canal-era regime shift (Broadberry et al. sectoral series)
  3. Canal mileage as a dose: levels, quadratic trend, first differences, horse race, reverse causality
  4. Benchmark-year comparison 1700 -> 1820 -> 1870
  5. NLP index as a stock proxy (ngram 'canal' vs cumulative miles)
  6. Sequencing: canal stock -> coal -> steam vocabulary (Granger-style local projections)

Usage:  python src/regime_analysis.py | tee docs/results_regime_v1.txt
"""
import warnings; warnings.filterwarnings('ignore')
from pathlib import Path
import numpy as np, pandas as pd, statsmodels.api as sm, statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parent.parent
EXT = ROOT / 'data' / 'external'
HAC = dict(cov_type='HAC', cov_kwds={'maxlags': 10})

b = pd.read_csv(EXT / 'boe_gb.csv').set_index('Year'); b['GDPpc'] = b['GDP'] / b['PopGB']
cum = pd.read_csv(EXT / 'canal_cum_miles.csv', index_col=0).iloc[:, 0]; cum.index = cum.index.astype(int)
panel = pd.read_csv(EXT / 'mpd_panel.csv')
w = np.exp(panel.pivot(index='year', columns='cc', values='lgdppc'))
lw = np.log(w)
ng = pd.read_csv(ROOT / 'data' / 'ngram_english.csv').set_index('Year')


def hdr(s): print('\n' + '=' * 78 + f'\n{s}\n' + '=' * 78)


def supwald(y, trim=0.15):
    """Quandt-Andrews sup-F for one break in level and trend. Returns (year, F)."""
    y = y.dropna(); yrs = y.index.values; n = len(y); t = np.arange(n); X0 = np.column_stack([np.ones(n), t])
    b0 = np.linalg.lstsq(X0, y.values, rcond=None)[0]; ssr0 = ((y.values - X0 @ b0) ** 2).sum(); best = (None, -1)
    for k in range(int(trim * n), int((1 - trim) * n)):
        d = (t >= k).astype(float); X1 = np.column_stack([X0, d, d * (t - k)])
        b1 = np.linalg.lstsq(X1, y.values, rcond=None)[0]; ssr1 = ((y.values - X1 @ b1) ** 2).sum()
        F = ((ssr0 - ssr1) / 2) / (ssr1 / (n - 4))
        if F > best[1]: best = (int(yrs[k]), round(float(F), 1))
    return best


def twobreak(y, minseg=20):
    y = y.dropna(); t = np.arange(len(y)); yrs = y.index.values; best = (None, None, np.inf)
    for k1 in range(minseg, len(y) - 2 * minseg):
        for k2 in range(k1 + minseg, len(y) - minseg):
            d1 = (t >= k1).astype(float); d2 = (t >= k2).astype(float)
            X = np.column_stack([np.ones(len(y)), t, d1, d1 * (t - k1), d2, d2 * (t - k2)])
            bb = np.linalg.lstsq(X, y.values, rcond=None)[0]; ssr = ((y.values - X @ bb) ** 2).sum()
            if ssr < best[2]: best = (int(yrs[k1]), int(yrs[k2]), ssr)
    return best[:2]


def trendchange(y, k, a=1700, bb=1830):
    s = y.loc[a:bb].dropna(); t = s.index.values.astype(float); d = (t >= k).astype(float)
    r = sm.OLS(s.values, sm.add_constant(np.column_stack([t, d * (t - k)]))).fit(**HAC)
    return r.params[1] * 100, r.params[2] * 100, r.pvalues[2]


# ---------------------------------------------------------------- 1. war confound
hdr('1. WAR CONFOUND IN THE CROSS-COUNTRY DiD (Maddison 2023, GDP per capita)')
print('Trend growth of log GDP per capita, %/yr')
for c in ['GBR', 'NLD', 'FRA', 'BEL', 'SWE', 'DEU', 'ESP']:
    print(f'  {c}: ' + '  '.join(f'{a}-{e}:{np.polyfit(lw.loc[a:e, c].index, lw.loc[a:e, c].values, 1)[0]*100:5.2f}' for a, e in [(1700, 1760), (1760, 1790), (1790, 1815), (1815, 1830), (1830, 1870)]))
print('\nPeak (1785-95) to trough (1795-1815) drawdown, and 1815 vs 1790')
for c in ['GBR', 'NLD', 'FRA', 'BEL', 'SWE', 'DEU', 'ESP', 'PRT', 'ITA']:
    pk = w.loc[1785:1795, c].max(); tr = w.loc[1795:1815, c].min()
    print(f'  {c}: peak {pk:6.0f} ({w.loc[1785:1795, c].idxmax()}) trough {tr:6.0f} ({w.loc[1795:1815, c].idxmin()}) drawdown {100*(tr/pk-1):6.1f}%  1815/1790 {100*(w.loc[1815, c]/w.loc[1790, c]-1):+5.1f}%')
gap = w['GBR'] - w[['NLD', 'FRA']].mean(axis=1)
print(f'\nSup-F break in GBR minus mean(NLD,FRA) log gap: {supwald(lw["GBR"] - lw[["NLD", "FRA"]].mean(axis=1))}')
print(f'Share of 1761-1900 level-gap growth (GBR vs NLD+FRA) occurring 1790-1815: {100*(gap[1815]-gap[1790])/(gap[1900]-gap[1761]):.0f}%')
print('Sup-F break GBR minus each control (log gdppc):', {c: supwald(lw['GBR'] - lw[c]) for c in ['NLD', 'FRA', 'SWE', 'DEU', 'ESP']})


def did(ycol, ctrls, t0=1761, a=1700, e=1900):
    s = panel[(panel.cc.isin(ctrls + ['GBR'])) & (panel.year >= a) & (panel.year <= e)].copy()
    s['did'] = ((s.cc == 'GBR') & (s.year >= t0)).astype(int)
    r = smf.ols(f'{ycol} ~ C(cc) + C(year) + did', s).fit(cov_type='HAC', cov_kwds={'maxlags': 15})
    return r.params['did'], r.pvalues['did'], len(s)


print('\nTWFE DiD on log GDP per capita, T0=1761, HAC(15) — note pre-trend failures in the event study below')
for name, ctrls in {'NLD+FRA': ['NLD', 'FRA'], 'FRA only': ['FRA'], 'FRA,SWE,DEU,ESP': ['FRA', 'SWE', 'DEU', 'ESP']}.items():
    for a, e in [(1700, 1790), (1700, 1810), (1700, 1900)]:
        b3, pv, n = did('lgdppc', ctrls, 1761, a, e); print(f'  {name:16s} {a}-{e}: beta={b3:6.3f} p={pv:.3f} N={n}')


def es(ctrls, bins=10, ref=1751):
    s = panel[panel.cc.isin(ctrls + ['GBR'])].copy(); s['treat'] = (s.cc == 'GBR').astype(int); s['bin'] = (s.year - 1761) // bins
    refbin = (ref - 1761) // bins
    form = 'lgdppc ~ C(cc) + C(year) + ' + ' + '.join(f'I(treat*(bin=={k}))' for k in sorted(s.bin.unique()) if k != refbin)
    r = smf.ols(form, s).fit(cov_type='HAC', cov_kwds={'maxlags': 15})
    return {1761 + k * bins: (r.params[f'I(treat * (bin == {k}))'], r.pvalues[f'I(treat * (bin == {k}))']) for k in sorted(s.bin.unique()) if k != refbin}


for name, ctrls in {'NLD+FRA': ['NLD', 'FRA'], 'FRA,SWE,DEU,ESP': ['FRA', 'SWE', 'DEU', 'ESP']}.items():
    print(f'\nEvent study (10y bins, ref 1751-60), GBR vs {name}:')
    print('   ' + '  '.join(f'{y}:{v:+.2f}({p:.2f})' for y, (v, p) in es(ctrls).items()))

# ---------------------------------------------------------------- 2. regime shift
hdr('2. BRITAIN: CANAL-ERA REGIME SHIFT (Broadberry et al. 2015 via Bank of England)')
lg = np.log(b)
print('Trend growth %/yr')
for a, e in [(1700, 1760), (1760, 1790), (1790, 1815), (1815, 1830), (1830, 1870)]:
    print(f'  {a}-{e}: ' + '  '.join(f'{c}={np.polyfit(lg.loc[a:e, c].dropna().index, lg.loc[a:e, c].dropna().values, 1)[0]*100:.2f}' for c in ['GDP', 'GDPpc', 'Ind', 'Agri', 'Serv', 'Coal', 'Iron', 'PopGB']))
print('\nTrend-slope change at 1761 (sample 1700-1830, HAC): pre-slope %/yr, change pp/yr, p')
for c in ['GDP', 'Ind', 'Coal', 'Iron', 'Textiles', 'Serv', 'PopGB', 'GDPpc', 'Agri']:
    pre, chg, p = trendchange(lg[c], 1761); print(f'  {c:9s}: {pre:5.2f} {chg:+5.2f} (p={p:.3f})')
print('\nSup-F single break (level+trend) 1700-1870 and best two breaks')
for c in ['GDP', 'Ind', 'Serv', 'Coal', 'Iron', 'Textiles', 'PopGB', 'GDPpc', 'Agri']:
    print(f'  {c:9s}: single {supwald(lg[c])}   two {twobreak(lg[c])}')
print('\nCoal output per capita, 1700=100:', ((b['Coal'] / b['PopGB']) / (b['Coal'] / b['PopGB']).loc[1700] * 100).loc[[1700, 1760, 1780, 1790, 1800, 1810, 1830, 1850]].round(0).to_dict())

# ---------------------------------------------------------------- 3. dose
hdr('3. CANAL MILEAGE AS A DOSE (Britain, 1700-1830, pre-railway)')
canals = pd.read_csv(EXT / 'uk_canals_wiki.csv')
dec = canals[(canals.year >= 1700) & (canals.year <= 1850)].groupby((canals.year // 10) * 10).miles.sum()
print('Canal miles opened per decade:', dec.round(0).astype(int).to_dict())
print('Cumulative miles:', cum.loc[[1760, 1770, 1780, 1790, 1800, 1810, 1820, 1830]].round(0).astype(int).to_dict())
steam = ng['steam'] / ng['steam'].loc[1830]
war = pd.Series(0, index=range(1700, 1901)); war.loc[1793:1815] = 1; war.loc[1756:1763] = 1; war.loc[1775:1783] = 1
t2 = pd.Series((np.arange(1700, 1901) - 1700.0) ** 2 / 1000, index=range(1700, 1901))


def reg(c, cols, a=1700, e=1830):
    y = lg[c].loc[a:e].dropna(); X = pd.DataFrame({'t': y.index.astype(float)}, index=y.index)
    for k, v in cols.items(): X[k] = v.reindex(y.index).values
    X = sm.add_constant(X.dropna()); return sm.OLS(y.loc[X.index], X).fit(**HAC)


print('\n(a) log y ~ trend + canal miles (000s)                 (b) + quadratic trend + war dummy                (c) horse race: + steam vocab (1830=1)')
for c in ['Coal', 'Ind', 'Iron', 'Serv', 'PopGB', 'GDP', 'GDPpc', 'Agri']:
    ra = reg(c, {'canal_k': cum / 1000}); rb = reg(c, {'canal_k': cum / 1000, 't2': t2, 'war': war}); rc = reg(c, {'canal_k': cum / 1000, 'steam': steam, 'war': war})
    print(f'  {c:6s}: (a) {100*ra.params["canal_k"]:6.1f}% p={ra.pvalues["canal_k"]:.3f} | (b) {100*rb.params["canal_k"]:6.1f}% p={rb.pvalues["canal_k"]:.3f} | (c) canal {100*rc.params["canal_k"]:6.1f}% p={rc.pvalues["canal_k"]:.3f}, steam {100*rc.params["steam"]:6.1f}% p={rc.pvalues["steam"]:.3f}')
dm = (cum / 1000).diff()
print('\n(d) First differences 1711-1830: Δlog y on Δmiles lags 0..10 (sum of coefficients, joint F)')
for c in ['Coal', 'Ind', 'PopGB', 'GDP', 'GDPpc', 'Agri']:
    dy = lg[c].diff(); Z = pd.concat([dm.shift(k).rename(f'l{k}') for k in range(0, 11)], axis=1)
    d = pd.concat([dy.rename('dy'), Z], axis=1).loc[1711:1830].dropna(); r = sm.OLS(d['dy'], sm.add_constant(d.drop(columns='dy'))).fit(**HAC)
    print(f'  {c:6s}: {100*r.params.drop("const").sum():+6.1f}% per 1,000 miles, joint p={float(r.f_test(np.eye(11, 12, 1)).pvalue):.3f}')
print('\n(e) Reverse causality: Δmiles_t on Σ_{k=1..10} Δlog y_{t-k}')
for c in ['Coal', 'Ind', 'GDP', 'PopGB']:
    dy = lg[c].diff(); Z = pd.concat([dy.shift(k).rename(f'l{k}') for k in range(1, 11)], axis=1)
    d = pd.concat([dm.rename('dm'), Z], axis=1).loc[1711:1830].dropna(); r = sm.OLS(d['dm'], sm.add_constant(d.drop(columns='dm'))).fit(**HAC)
    print(f'  {c:6s}: sum={r.params.drop("const").sum():+.3f}, joint p={float(r.f_test(np.eye(10, 11, 1)).pvalue):.3f}')

# ---------------------------------------------------------------- 4. benchmarks
hdr('4. BENCHMARK YEARS 1700 -> 1820 -> 1870 (Maddison 2023; population is real only at benchmarks)')
pp = np.exp(panel.pivot(index='year', columns='cc', values='lpop')); tt = np.exp(panel.pivot(index='year', columns='cc', values='ltot'))
print(f'{"cc":4s} {"gdppc 1700-1820":>16s} {"pop":>8s} {"total GDP":>10s} | {"gdppc 1820-70":>14s} {"pop":>8s}')
for c in ['GBR', 'NLD', 'FRA', 'BEL', 'SWE', 'DEU', 'ESP', 'PRT', 'CHN', 'JPN']:
    print(f'{c:4s} {100*(w.loc[1820, c]/w.loc[1700, c]-1):+15.0f}% {100*(pp.loc[1820, c]/pp.loc[1700, c]-1):+7.0f}% {100*(tt.loc[1820, c]/tt.loc[1700, c]-1):+9.0f}% | {100*(w.loc[1870, c]/w.loc[1820, c]-1):+13.0f}% {100*(pp.loc[1870, c]/pp.loc[1820, c]-1):+7.0f}%')

# ---------------------------------------------------------------- 5. NLP stock proxy
hdr('5. NLP INDEX AS A STOCK PROXY (eng_gb_2019 "canal" vs canal network)')
yr = cum.diff().fillna(cum.iloc[0]); op10 = yr.rolling(10, center=True).sum(); c_ng = ng['canal']
print(f'corr(ngram canal, cumulative miles) 1740-1850:        {np.corrcoef(c_ng.loc[1740:1850], cum.loc[1740:1850])[0, 1]:.2f}')
print(f'corr(ngram canal, miles opened in 10y window) 1740-1850: {np.corrcoef(c_ng.loc[1745:1845], op10.loc[1745:1845])[0, 1]:.2f}')
print('Peaks of canal-related vocabulary:', {k: int(ng[k].idxmax()) for k in ['canal', 'navigation', 'inland navigation', 'canal navigation']})

# ---------------------------------------------------------------- 6. sequencing
hdr('6. SEQUENCING: canal stock -> coal output -> steam (local projections, 1700-1830)')
def lp(y, x, horizons=(5, 10, 15, 20), a=1700, e=1830):
    out = []
    for h in horizons:
        d = pd.concat([(y.shift(-h) - y).rename('dy'), x.rename('x'), y.rename('y0')], axis=1); d['t'] = d.index.astype(float); d = d.loc[a:e - h].dropna()
        r = sm.OLS(d['dy'], sm.add_constant(d[['x', 'y0', 't']])).fit(**HAC); out.append(f'h={h}: {r.params["x"]:+.3f} (p={r.pvalues["x"]:.3f})')
    return '  '.join(out)
print('Δ_h log coal on canal stock (000 miles), controlling level and trend:   ', lp(lg['Coal'], cum / 1000))
print('Δ_h log steam-vocab on canal stock:                                   ', lp(np.log(ng['steam'].replace(0, np.nan)).dropna(), cum / 1000))
print('Δ_h log steam-vocab on log coal output:                               ', lp(np.log(ng['steam'].replace(0, np.nan)).dropna(), lg['Coal']))
print('Δ_h log GDP per capita on canal stock:                                ', lp(lg['GDPpc'], cum / 1000))
print('Δ_h log GDP per capita on log steam-vocab:                            ', lp(lg['GDPpc'], np.log(ng['steam'].replace(0, np.nan))))
print('\nReading: canals -> coal -> steam -> per-capita income is the precondition chain (Tvedt 2010).')
