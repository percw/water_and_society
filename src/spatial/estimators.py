#!/usr/bin/env python3
"""
Estimators for the spatial design (expansion/spatial/PRE_ANALYSIS_PLAN.md).

All three analyses share one estimator: a stacked event study (Cengiz, Dube, Lindner and Zipperer 2019)
around the year a place is first connected to the navigable-waterway network. For each connection
cohort g, the stack holds the units connected in g and clean controls (never connected, or connected
more than `window[1]` years after g), restricted to event time window[0]..window[1]. Unit-by-stack and
year-by-stack fixed effects are absorbed by alternating projections; standard errors are clustered on
the original unit. Staggered timing therefore never uses already-treated units as controls, which is
the bias two-way fixed effects suffer from (Goodman-Bacon 2021; Sun and Abraham 2021).

  event_study(df, ...)        -> event-time coefficients (reference e = -1)
  event_study(df, by='coal')  -> the same, separately by a binary moderator, plus the difference
  national_counterfactual(..) -> share of national growth attributable to connection (macro bridge)
  simulate(...)               -> synthetic panel with a known effect, for testing

Run this file to check that the estimator recovers a known effect and flat pre-trends.
"""
import numpy as np, pandas as pd


def _stack(df, unit, time, g, window, max_rel=None):
    lo, hi = window
    cohorts = sorted(df.loc[df[g].notna(), g].unique())
    units_g = df.groupby(unit)[g].first()
    out = []
    for c in cohorts:
        treated = units_g.index[units_g == c]
        clean = units_g.index[units_g.isna() | (units_g > c + hi)]
        if len(treated) == 0 or len(clean) == 0:
            continue
        s = df[df[unit].isin(treated.union(clean)) & df[time].between(c + lo, c + hi)].copy()
        s['_stack'] = c; s['_treated'] = s[unit].isin(treated).astype(int); s['_e'] = s[time] - c
        out.append(s)
    return pd.concat(out, ignore_index=True)


def _demean(X, groups, tol=1e-10, max_iter=500):
    """Absorb several sets of fixed effects by alternating projections."""
    X = X.copy()
    for _ in range(max_iter):
        delta = 0.0
        for gid in groups:
            means = X.groupby(gid).transform('mean'); X -= means; delta = max(delta, float(np.abs(means.values).max()))
        if delta < tol:
            break
    return X


def _cluster_ols(y, X, cl):
    XtX_inv = np.linalg.pinv(X.T @ X); b = XtX_inv @ X.T @ y; u = y - X @ b
    meat = np.zeros((X.shape[1], X.shape[1]))
    for _, idx in pd.Series(np.arange(len(y))).groupby(cl.values):
        s = X[idx.values].T @ u[idx.values]; meat += np.outer(s, s)
    G = cl.nunique(); n, k = X.shape
    V = XtX_inv @ meat @ XtX_inv * G / (G - 1) * (n - 1) / (n - k)
    return b, V


def event_study(df, unit='unit', time='year', outcome='y', g='connect_year', window=(-10, 20), by=None, ref=-1):
    """Stacked event study. With `by` (a 0/1 unit-level column), estimates the event path separately
    for by == 0 and by == 1 in one regression and reports their difference."""
    s = _stack(df, unit, time, g, window)
    es = [e for e in range(window[0], window[1] + 1) if e != ref]
    cols = {}
    groups_by = [None] if by is None else [0, 1]
    for k in groups_by:
        for e in es:
            m = (s['_treated'] == 1) & (s['_e'] == e)
            if k is not None:
                m &= (s[by] == k)
            cols[(k, e)] = m.astype(float)
    X = pd.DataFrame({f'{k}_{e}': v for (k, e), v in cols.items()})
    Y = s[[outcome]].reset_index(drop=True)
    su, st = s[unit].astype(str) + '|' + s['_stack'].astype(str), s[time].astype(str) + '|' + s['_stack'].astype(str)
    if by is not None:   # year effects may differ by moderator group (e.g. coalfield regions)
        st = st + '|' + s[by].astype(str)
    Z = _demean(pd.concat([Y, X], axis=1), [su.values, st.values])
    b, V = _cluster_ols(Z[outcome].values, Z.drop(columns=outcome).values, s[unit].reset_index(drop=True))
    names = list(X.columns); se = np.sqrt(np.diag(V))
    res = pd.DataFrame({'name': names, 'coef': b, 'se': se})
    res['group'] = [None if n.startswith('None') else int(n.split('_')[0]) for n in names]
    res['e'] = [int(n.split('_')[1]) for n in names]
    if by is not None:
        diff = []
        for e in es:
            i, j = names.index(f'1_{e}'), names.index(f'0_{e}')
            w = np.zeros(len(b)); w[i], w[j] = 1, -1
            diff.append({'name': f'diff_{e}', 'coef': b[i] - b[j], 'se': float(np.sqrt(w @ V @ w)), 'group': 'diff', 'e': e})
        res = pd.concat([res, pd.DataFrame(diff)], ignore_index=True)
    res['lo'], res['hi'] = res.coef - 1.96 * res.se, res.coef + 1.96 * res.se
    return res.drop(columns='name'), V, names


def pretrend_test(res, V, names, window_pre):
    """Joint Wald test that all pre-period coefficients are zero."""
    idx = [i for i, n in enumerate(names) if window_pre[0] <= int(n.split('_')[1]) <= window_pre[1]]
    b = res.loc[idx, 'coef'].values; Vp = V[np.ix_(idx, idx)]
    from scipy import stats
    W = float(b @ np.linalg.pinv(Vp) @ b); return W, float(stats.chi2.sf(W, len(idx)))


def national_counterfactual(df, effects, unit='unit', time='year', level='pop', g='connect_year'):
    """Remove the estimated log effect of connection from every connected unit and re-aggregate.
    Returns national totals with and without connection effects, and the share of national growth
    between the first and last year that connection accounts for."""
    eff = effects.set_index('e')['coef']
    d = df[[unit, time, level, g]].copy(); d['e'] = d[time] - d[g]
    emax = eff.index.max(); d['beta'] = np.where(d[g].isna() | (d['e'] < 0), 0.0, d['e'].clip(upper=emax).map(eff).fillna(0.0))
    d['cf'] = d[level] * np.exp(-d['beta'])
    tot = d.groupby(time)[[level, 'cf']].sum()
    t0, t1 = tot.index.min(), tot.index.max()
    share = 1 - (tot.loc[t1, 'cf'] - tot.loc[t0, 'cf']) / (tot.loc[t1, level] - tot.loc[t0, level])
    return tot, float(share)


def simulate(n=404, years=(1700, 1837), effect=0.10, ramp=10, share_connected=0.6, moderator_share=0.5,
             effect_if_moderator0=None, seed=1):
    """Synthetic parish panel: unit and year effects, AR(1) noise, staggered connection 1760-1830.
    The effect ramps linearly to `effect` (log points) over `ramp` years. If effect_if_moderator0 is given,
    units with moderator 0 get that effect instead (tests the complementarity design)."""
    rng = np.random.default_rng(seed); T = np.arange(years[0], years[1] + 1)
    g = np.where(rng.random(n) < share_connected, rng.integers(1760, 1831, n), np.nan)
    mod = (rng.random(n) < moderator_share).astype(int)
    a = rng.normal(0, 1, n); yfe = np.cumsum(rng.normal(0.004, 0.01, len(T)))
    rows = []
    for i in range(n):
        eps = 0.0; eff_i = effect if (effect_if_moderator0 is None or mod[i] == 1) else effect_if_moderator0
        for t in T:
            eps = 0.5 * eps + rng.normal(0, 0.05)
            e = t - g[i] if not np.isnan(g[i]) else -999
            tau = 0.0 if e < 0 else eff_i * min(1.0, (e + 1) / ramp)
            rows.append((i, t, a[i] + yfe[t - T[0]] + tau + eps, g[i], mod[i]))
    d = pd.DataFrame(rows, columns=['unit', 'year', 'y', 'connect_year', 'coal']); d['pop'] = np.exp(d['y'] + 6)
    return d


if __name__ == '__main__':
    d = simulate()
    res, V, names = event_study(d, window=(-10, 20))
    W, p = pretrend_test(res, V, names, (-10, -2))
    post = res[res.e >= 10].coef.mean()
    print(f'Simulation, true effect 0.10 after 10 years: estimated mean over e>=10 = {post:.3f}; pre-trend Wald p = {p:.2f}')
    assert abs(post - 0.10) < 0.02 and p > 0.01
    d2 = simulate(effect_if_moderator0=0.0, seed=2)
    r2, V2, n2 = event_study(d2, window=(-10, 20), by='coal')
    diff = r2[(r2.group == 'diff') & (r2.e >= 10)].coef.mean(); zero = r2[(r2.group == 0) & (r2.e >= 10)].coef.mean()
    print(f'Complementarity: effect only near coal (0.10): difference = {diff:.3f}, effect away from coal = {zero:.3f}')
    assert abs(diff - 0.10) < 0.03 and abs(zero) < 0.03
    tot, share = national_counterfactual(d, res[res.group.isna()])
    print(f'Macro bridge on the simulated panel: share of total growth attributable to connection = {share:.1%}')
    print('All estimator checks passed.')
