#!/usr/bin/env python3
"""
Mechanism analysis: the precondition chain  canals -> coal -> steam -> per-capita income.

Extends regime_analysis.py with
  7. Power capacity: steam vs water horsepower (Kanefsky 1979 via Crafts 2004), interpolated
  8. Local projections along the chain, with steam measured as installed horsepower
  9. Mediation: canal stock -> coal output -> industrial output / population (block bootstrap)
 10. Semantic sequencing: coal-by-water bigrams vs coal-by-steam bigrams (Google Books eng_gb_2019)
 11. Authorisation series from Priestley (1831), if parsed

Estimator choice. The within-Britain sample is ~130 annual observations of smooth, trending series.
Linear local projections and distributed lags with HAC errors are the appropriate tool here; a
Double/Debiased ML estimator with tree learners over-fits the year trend on a sample this small and
collapses the treatment residual (the failure mode already documented in dml_analysis.py). DML is
therefore retained only for the cross-country panel in dml_analysis.py, and the mediation here is
linear with a moving-block bootstrap for inference.

Usage:  python src/mechanism_analysis.py | tee docs/results_mechanism_v1.txt
"""
import warnings; warnings.filterwarnings('ignore')
from pathlib import Path
import numpy as np, pandas as pd, statsmodels.api as sm

ROOT = Path(__file__).resolve().parent.parent; EXT = ROOT / 'data' / 'external'
HAC = dict(cov_type='HAC', cov_kwds={'maxlags': 10}); rng = np.random.default_rng(1761)

b = pd.read_csv(EXT / 'boe_gb.csv').set_index('Year'); b['GDPpc'] = b['GDP'] / b['PopGB']; lg = np.log(b)
cum = pd.read_csv(EXT / 'canal_cum_miles.csv', index_col=0).iloc[:, 0]; cum.index = cum.index.astype(int); canal_k = cum / 1000
ng = pd.read_csv(ROOT / 'data' / 'ngram_english.csv').set_index('Year')
bg = pd.read_csv(EXT / 'ngram_bigrams_coal_transport.csv').set_index('Year')
hp = pd.read_csv(EXT / 'power_hp.csv').set_index('Year').loc[1760:1870]


def hdr(s): print('\n' + '=' * 78 + f'\n{s}\n' + '=' * 78)


# ---------------------------------------------------------------- 7. power capacity
hdr('7. INSTALLED POWER: STEAM vs WATER HORSEPOWER (Kanefsky 1979 via Crafts 2004)')
idx = range(1760, 1871)
lhp = np.log(hp[['steam_hp_k', 'water_hp_k']]).reindex(idx).interpolate(method='index')
steam_hp = np.exp(lhp['steam_hp_k']); water_hp = np.exp(lhp['water_hp_k'])
share = steam_hp / (steam_hp + water_hp + np.exp(np.log(hp['wind_hp_k']).reindex(idx).interpolate(method='index')))
print(hp[['steam_hp_k', 'water_hp_k', 'wind_hp_k']].to_string())
print('\nSteam share of stationary power (interpolated):', {y: f'{share.loc[y]:.0%}' for y in [1760, 1780, 1800, 1810, 1820, 1830, 1840, 1850, 1870]})
cross = share[share >= 0.5].index.min(); print(f'Steam overtakes water + wind: {cross}')
print('Coal output per unit of installed steam hp (1760=100), i.e. how much coal moved without steam:',
      {y: round(float((b.loc[y, 'Coal'] / steam_hp.loc[y]) / (b.loc[1760, 'Coal'] / steam_hp.loc[1760]) * 100)) for y in [1760, 1780, 1800, 1830, 1850, 1870]})

# ---------------------------------------------------------------- 8. local projections
hdr('8. LOCAL PROJECTIONS ALONG THE CHAIN (1760-1830 for steam hp; 1700-1830 otherwise)')


def lp(y, x, horizons=(5, 10, 15, 20), a=1700, e=1830, controls=None):
    out = []
    for h in horizons:
        d = pd.concat([(y.shift(-h) - y).rename('dy'), x.rename('x'), y.rename('y0')] + ([c.rename(f'c{i}') for i, c in enumerate(controls)] if controls else []), axis=1)
        d['t'] = d.index.astype(float); d = d.loc[a:e - h].dropna()
        r = sm.OLS(d['dy'], sm.add_constant(d.drop(columns='dy'))).fit(**HAC)
        out.append((h, r.params['x'], r.bse['x'], r.pvalues['x']))
    return out


def show(label, res):
    print(f'{label:58s}' + '  '.join(f'h={h}: {b_:+.3f} (p={p:.3f})' for h, b_, se, p in res))


lsteam = np.log(steam_hp); lwater = np.log(water_hp)
show('Δ_h log coal        on canal stock (000 mi)', lp(lg['Coal'], canal_k))
show('Δ_h log coal        on canal stock, + log steam hp control', lp(lg['Coal'], canal_k, a=1760, controls=[lsteam]))
show('Δ_h log steam hp    on canal stock', lp(lsteam, canal_k, a=1760))
show('Δ_h log steam hp    on log coal output', lp(lsteam, lg['Coal'], a=1760))
show('Δ_h log steam hp    on log coal, + canal stock control', lp(lsteam, lg['Coal'], a=1760, controls=[canal_k]))
show('Δ_h log water hp    on canal stock', lp(lwater, canal_k, a=1760))
show('Δ_h log industry    on canal stock', lp(lg['Ind'], canal_k))
show('Δ_h log industry    on log steam hp', lp(lg['Ind'], lsteam, a=1760))
show('Δ_h log GDP/capita  on canal stock', lp(lg['GDPpc'], canal_k))
show('Δ_h log GDP/capita  on log steam hp', lp(lg['GDPpc'], lsteam, a=1760))
show('Δ_h log GDP/capita  on log steam hp, sample 1760-1870', lp(lg['GDPpc'], lsteam, a=1760, e=1870))
show('Δ_h log population  on canal stock', lp(lg['PopGB'], canal_k))
show('Δ_h log agriculture on canal stock (placebo)', lp(lg['Agri'], canal_k))
# save IRFs for figures
irf = []
for lab, y, x, a in [('canal→coal', lg['Coal'], canal_k, 1700), ('canal→steam hp', lsteam, canal_k, 1760), ('coal→steam hp', lsteam, lg['Coal'], 1760), ('canal→GDP per capita', lg['GDPpc'], canal_k, 1700), ('steam hp→GDP per capita', lg['GDPpc'], lsteam, 1760), ('canal→agriculture', lg['Agri'], canal_k, 1700)]:
    for h, b_, se, p in lp(y, x, horizons=tuple(range(1, 21)), a=a): irf.append((lab, h, b_, se, p))
pd.DataFrame(irf, columns=['chain', 'h', 'beta', 'se', 'p']).to_csv(EXT / 'lp_irfs.csv', index=False)

# ---------------------------------------------------------------- 9. mediation
hdr('9. MEDIATION: canal stock -> coal -> outcome (linear, 1700-1830, moving-block bootstrap)')


def mediation(Y, M, X, a=1700, e=1830, nboot=2000, block=10):
    d = pd.concat([Y.rename('Y'), M.rename('M'), X.rename('X')], axis=1); d['t'] = d.index.astype(float); d['t2'] = (d.t - 1700) ** 2 / 1000
    d = d.loc[a:e].dropna()
    def fit(dd):
        c_tot = sm.OLS(dd.Y, sm.add_constant(dd[['X', 't', 't2']])).fit().params['X']
        a_ = sm.OLS(dd.M, sm.add_constant(dd[['X', 't', 't2']])).fit().params['X']
        r = sm.OLS(dd.Y, sm.add_constant(dd[['X', 'M', 't', 't2']])).fit().params
        return c_tot, a_ * r['M'], r['X']
    tot, ind, dir_ = fit(d); n = len(d); boots = []
    for _ in range(nboot):
        starts = rng.integers(0, n - block, size=n // block + 1)
        idx_ = np.concatenate([np.arange(s, s + block) for s in starts])[:n]
        boots.append(fit(d.iloc[idx_]))
    boots = np.array(boots); lo, hi = np.percentile(boots, [2.5, 97.5], axis=0)
    return tot, ind, dir_, lo, hi


for yl, Y in [('industry', lg['Ind']), ('population', lg['PopGB']), ('GDP per capita', lg['GDPpc']), ('services', lg['Serv'])]:
    tot, ind, dir_, lo, hi = mediation(Y, lg['Coal'], canal_k)
    print(f'{yl:15s}: total {100*tot:+6.1f}% [{100*lo[0]:+.1f},{100*hi[0]:+.1f}] | via coal {100*ind:+6.1f}% [{100*lo[1]:+.1f},{100*hi[1]:+.1f}] | direct {100*dir_:+6.1f}% [{100*lo[2]:+.1f},{100*hi[2]:+.1f}] | mediated share {ind/tot if abs(tot)>1e-9 else float("nan"):.0%}')
print('(effects per 1,000 canal miles, quadratic trend controlled; 95% block-bootstrap intervals)')
print('Reading: with a quadratic trend absorbed, the mediation decomposition is NOT identified on 130 annual observations —\n         intervals span zero for every path. The sequencing evidence rests on the local projections (section 8), not on this table.')

# ---------------------------------------------------------------- 10. semantic sequencing
hdr('10. SEMANTIC SEQUENCING: coal moved by water before coal burned in engines (eng_gb_2019 bigrams)')
norm = lambda cols: sum(bg[c] / bg[c].loc[1850] for c in cols) / len(cols)   # equal-weight index, each term = 1 in 1850
g_water = norm(['coal barge', 'coal wharf', 'coal boat', 'canal boat'])
g_steam = norm(['steam engine', 'steam power', 'steam boat'])
sm5 = lambda s: s.rolling(5, center=True).mean()


def threshold_year(s, frac, ref=1850):
    s = sm5(s); lvl = s.loc[ref] * frac; hit = s[(s.index <= ref) & (s >= lvl)]; return int(hit.index.min()) if len(hit) else None


print(f'{"series":32s} {"10% of 1850":>12s} {"25%":>6s} {"50%":>6s}')
for lab, s in [('coal-by-water bigrams', g_water), ('canal boat', bg['canal boat']), ('coal wharf', bg['coal wharf']), ('coal barge', bg['coal barge']), ('"canal" (unigram)', ng['canal']), ('coal-by-steam bigrams', g_steam), ('steam engine', bg['steam engine']), ('steam power', bg['steam power']), ('coal field', bg['coal field']), ('fire engine (18th-c. term)', bg['fire engine'])]:
    print(f'{lab:32s} {str(threshold_year(s, .10)):>12s} {str(threshold_year(s, .25)):>6s} {str(threshold_year(s, .50)):>6s}')
fe, se_ = sm5(bg['fire engine']), sm5(bg['steam engine']); sw = se_[(se_ > fe) & (se_.index >= 1740)].index.min()
print(f'\n"steam engine" overtakes "fire engine" in print: {sw}')
wc = sm5(bg['water carriage']); lc = sm5(bg['land carriage']); print(f'"water carriage"/"land carriage" ratio: 1750 {wc.loc[1750]/lc.loc[1750]:.2f}, 1790 {wc.loc[1790]/lc.loc[1790]:.2f}, 1810 {wc.loc[1810]/lc.loc[1810]:.2f}, 1840 {wc.loc[1840]/lc.loc[1840]:.2f}')
xc = [(k, np.corrcoef(np.log1p(g_water.loc[1760:1850] * 1e9), np.log1p(g_steam.shift(k).loc[1760:1850] * 1e9))[0, 1]) for k in range(-30, 31, 5)]
print('Cross-correlation log coal-by-water_t with log coal-by-steam_{t-k} (k<0: steam leads; k>0: water leads):', '  '.join(f'k={k}:{c:.2f}' for k, c in xc))
pd.DataFrame({'coal_by_water': g_water, 'coal_by_steam': g_steam, 'fire_engine': bg['fire engine'], 'steam_engine': bg['steam engine'], 'canal': ng['canal']}).to_csv(EXT / 'semantic_sequence.csv')

# ---------------------------------------------------------------- 11. Priestley
hdr('11. PARLIAMENTARY AUTHORISATION (Priestley 1831, OCR-parsed; provisional)')
pf = EXT / 'priestley_1831_acts.csv'
if pf.exists():
    p = pd.read_csv(pf); print(f'{len(p)} navigations with regnal act years parsed; first-act decade counts (canals only):')
    pc = p[p.navigation.str.contains('CANAL')]; print(pc.groupby((pc.first_act // 10) * 10).size().to_string()); print(f'canals first authorised 1760-1829: {((pc.first_act>=1760)&(pc.first_act<1830)).sum()}, of which 1790-1799: {((pc.first_act>=1790)&(pc.first_act<1800)).sum()}')
else:
    print('not available')

# ---------------------------------------------------------------- 12. predetermined doses
hdr('12. PREDETERMINED DOSES (referee check on reverse causality)')
print('Canals were built where demand was growing (regime_analysis §3e). Two doses fixed before the outcome window:')
print('  (i) completion-based canal stock lagged 10 and 15 years; (ii) cumulative count of navigations first AUTHORISED by')
print('  Parliament (Priestley 1831), lagged 10 years — authorisation precedes opening by ~7 years and cannot respond to later output.')
pr = pd.read_csv(EXT / 'priestley_1831_acts.csv'); prc = pr[pr.navigation.str.contains('CANAL')]
auth = pd.Series(0.0, index=range(1700, 1901)); auth.update(prc.groupby('first_act').size().astype(float)); auth_cum = auth.cumsum()
t2 = pd.Series((np.arange(1700, 1901) - 1700.0) ** 2 / 1000, index=range(1700, 1901))


def dose_reg(y, x, a=1700, e=1830, quad=False):
    d = pd.concat([y.rename('y'), x.rename('x')], axis=1); d['t'] = d.index.astype(float)
    if quad: d['t2'] = t2.reindex(d.index)
    d = d.loc[a:e].dropna(); r = sm.OLS(d['y'], sm.add_constant(d.drop(columns='y'))).fit(**HAC)
    return r.params['x'], r.pvalues['x']


print(f'\n{"outcome":10s} {"miles lag10":>22s} {"miles lag15":>22s} {"auth count lag10 (per 10 canals)":>34s} {"auth lag10 + quad trend":>24s}')
for c in ['Coal', 'Ind', 'PopGB', 'Serv', 'GDPpc', 'Agri']:
    r1 = dose_reg(lg[c], canal_k.shift(10), a=1710); r2 = dose_reg(lg[c], canal_k.shift(15), a=1715)
    r3 = dose_reg(lg[c], auth_cum.shift(10) / 10, a=1710); r4 = dose_reg(lg[c], auth_cum.shift(10) / 10, a=1710, quad=True)
    print(f'{c:10s} {100*r1[0]:+8.1f}% (p={r1[1]:.3f})   {100*r2[0]:+8.1f}% (p={r2[1]:.3f})   {100*r3[0]:+8.1f}% (p={r3[1]:.3f})               {100*r4[0]:+8.1f}% (p={r4[1]:.3f})')
print('\nLocal projections with the authorisation count (per 10 canals authorised, lagged 10 years):')
show('Δ_h log coal        on authorised canals (lag 10)', lp(lg['Coal'], auth_cum.shift(10) / 10, a=1710))
show('Δ_h log population  on authorised canals (lag 10)', lp(lg['PopGB'], auth_cum.shift(10) / 10, a=1710))
show('Δ_h log GDP/capita  on authorised canals (lag 10)', lp(lg['GDPpc'], auth_cum.shift(10) / 10, a=1710))
show('Δ_h log agriculture on authorised canals (lag 10)', lp(lg['Agri'], auth_cum.shift(10) / 10, a=1710))
print('Reverse check: Δ authorisations_t on Σ_{k=1..10} Δlog coal_{t-k}:')
dy = lg['Coal'].diff(); Z = pd.concat([dy.shift(k).rename(f'l{k}') for k in range(1, 11)], axis=1)
d = pd.concat([auth.rename('da'), Z], axis=1).loc[1711:1830].dropna(); r = sm.OLS(d['da'], sm.add_constant(d.drop(columns='da'))).fit(**HAC)
print(f'  sum coef={r.params.drop("const").sum():+.2f}, joint p={float(r.f_test(np.eye(10, 11, 1)).pvalue):.3f}')

# ---------------------------------------------------------------- 13. steam link without interpolated horsepower
hdr('13. STEAM LINK WITH AN INDEPENDENT STEAM MEASURE (print frequency of "steam engine")')
lse = np.log(bg['steam engine'].replace(0, np.nan)).dropna()
show('Δ_h log "steam engine" on canal stock', lp(lse, canal_k, a=1740))
show('Δ_h log "steam engine" on log coal output', lp(lse, lg['Coal'], a=1740))
show('Δ_h log "steam engine" on log coal, + canal control', lp(lse, lg['Coal'], a=1740, controls=[canal_k]))
show('Δ_h log GDP/capita  on log "steam engine", 1740-1830', lp(lg['GDPpc'], lse, a=1740))
show('Δ_h log GDP/capita  on log "steam engine", 1740-1870', lp(lg['GDPpc'], lse, a=1740, e=1870))
print(f'corr(log steam hp interpolated, log "steam engine" freq) 1760-1870: {np.corrcoef(lsteam.loc[1760:1870], lse.loc[1760:1870])[0,1]:.2f}')

# ---------------------------------------------------------------- 14. semantic thresholds: robustness
hdr('14. SEMANTIC THRESHOLD ROBUSTNESS (smoothing window x reference year)')


def thr(s, frac, ref, win):
    s = s.rolling(win, center=True).mean(); lvl = s.loc[ref] * frac; hit = s[(s.index <= ref) & (s >= lvl)]; return int(hit.index.min()) if len(hit) else None


print(f'{"series":22s} ' + '  '.join(f'{"25%/"+str(ref)+"/w"+str(win):>14s}' for ref in (1850, 1830) for win in (3, 5, 9)))
for lab, s in [('coal barge', bg['coal barge']), ('coal wharf', bg['coal wharf']), ('canal (unigram)', ng['canal']), ('coal-by-water group', g_water), ('steam engine', bg['steam engine']), ('steam power', bg['steam power']), ('coal-by-steam group', g_steam)]:
    print(f'{lab:22s} ' + '  '.join(f'{str(thr(s, .25, ref, win)):>14s}' for ref in (1850, 1830) for win in (3, 5, 9)))
