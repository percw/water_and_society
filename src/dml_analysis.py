"""
dml_analysis.py — Double/Debiased Machine Learning (DML) Causal Analysis

Implements Chernozhukov et al. (2018) partially linear model:

    Y = θ·D + g(X) + ε

Where:
    Y = GDP per capita (outcome)
    D = hydro-social vocabulary intensity × GBR indicator (continuous treatment)
    X = confounders (country FE, year trends, population, etc.)
    θ = causal effect of the hydro-social linguistic shift on GDP

The partial-out (Frisch-Waugh-Lovell + ML) approach:
    1. ML-predict Y from X → residual ε_Y = Y - ĝ(X)
    2. ML-predict D from X → residual ε_D = D - m̂(X)
    3. OLS: ε_Y = θ · ε_D + error

Cross-fitting (K-fold) ensures valid inference even when ML overfits.

Key advantage over collapsed DiD:
    - Exploits continuous variation in treatment intensity (not just binary)
    - Valid standard errors without country-level clustering
    - Robust to model misspecification via ML nuisance estimation

Usage:
    python dml_analysis.py             # Full DML analysis
    python dml_analysis.py --n-splits 10  # More cross-fitting folds

References:
    Chernozhukov et al. (2018), "Double/Debiased Machine Learning"
    Robins et al. (1994), "Estimation of Regression Coefficients..."
"""

import argparse
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path
from scipy import stats

warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)

# ── Paths ────────────────────────────────────────────────────────────────────
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

# ── Import shared config from did_analysis ───────────────────────────────────
from did_analysis import (
    ALL_COUNTRIES, CONTROLS_EUR_EXT, CONTROLS_ASIA, COUNTRY_LABELS,
    AGRARIAN_WORDS, INDUSTRIAL_WORDS,
    CH_TRANSPORT, CH_POWER, CH_MANUFACTURING,
    PLACEBO_STEAM_MECH,
    fetch_real_maddison, derive_treatment_year,
)


# ─────────────────────────────────────────────────────────────────────────────
# 1. Build DML Panel with Continuous Treatment
# ─────────────────────────────────────────────────────────────────────────────

def build_dml_panel(df_gdp, df_ngram, channel='composite'):
    """Build panel with continuous treatment intensity.

    Treatment D_it = vocab_intensity_t × 1(country=GBR)

    For GBR: D varies continuously over time as vocabulary shifts.
    For controls: D = 0 (they don't experience the English linguistic shift).

    Channels:
        'composite'   — Industrial / (Agrarian + Industrial) ratio
        'transport'   — Canal/transport vocabulary intensity
        'power'       — Water wheel/power vocabulary intensity
        'canal_only'  — Just the word 'canal' frequency (most parsimonious)
    """
    # Compute treatment intensity from Ngram data
    if channel == 'composite':
        agrarian = [w for w in AGRARIAN_WORDS if w in df_ngram.columns]
        industrial = [w for w in INDUSTRIAL_WORDS if w in df_ngram.columns]
        a_sum = df_ngram[agrarian].sum(axis=1)
        i_sum = df_ngram[industrial].sum(axis=1)
        intensity = i_sum / (a_sum + i_sum)
        intensity.name = 'vocab_intensity'
    elif channel == 'transport':
        transport = [w for w in CH_TRANSPORT if w in df_ngram.columns]
        if not transport:
            print(f"  ⚠ No transport terms found. Available: {df_ngram.columns.tolist()[:10]}...")
            return None
        intensity = df_ngram[transport].sum(axis=1)
        # Normalize to [0, 1]
        intensity = (intensity - intensity.min()) / (intensity.max() - intensity.min())
        intensity.name = 'transport_intensity'
    elif channel == 'power':
        power = [w for w in CH_POWER if w in df_ngram.columns]
        if not power:
            return None
        intensity = df_ngram[power].sum(axis=1)
        intensity = (intensity - intensity.min()) / (intensity.max() - intensity.min())
        intensity.name = 'power_intensity'
    elif channel == 'canal_only':
        if 'canal' not in df_ngram.columns:
            return None
        intensity = df_ngram['canal']
        intensity = (intensity - intensity.min()) / (intensity.max() - intensity.min())
        intensity.name = 'canal_intensity'
    elif channel == 'steam':
        steam = [w for w in PLACEBO_STEAM_MECH if w in df_ngram.columns]
        if not steam:
            return None
        intensity = df_ngram[steam].sum(axis=1)
        intensity = (intensity - intensity.min()) / (intensity.max() - intensity.min())
        intensity.name = 'steam_intensity'
    else:
        raise ValueError(f"Unknown channel: {channel}")

    # Build panel
    countries = [c for c in ALL_COUNTRIES if c in df_gdp.columns]
    years = df_gdp.index

    rows = []
    for year in years:
        if year not in intensity.index:
            continue
        d_year = float(intensity.loc[year])
        for c in countries:
            if year not in df_gdp.index:
                continue
            gdp = df_gdp.loc[year, c]
            if pd.isna(gdp):
                continue

            is_gbr = 1 if c == 'GBR' else 0
            rows.append({
                'Year': int(year),
                'Country': c,
                'GDP_per_Capita': float(gdp),
                'log_GDP': float(np.log(max(gdp, 1))),
                'Treated': is_gbr,
                'Vocab_Intensity': d_year,
                'D': d_year * is_gbr,  # Continuous treatment
                'Year_centered': int(year) - 1800,
                'Year_sq': (int(year) - 1800) ** 2,
            })

    panel = pd.DataFrame(rows)

    # Add country dummies
    for c in countries:
        panel[f'C_{c}'] = (panel['Country'] == c).astype(int)

    return panel


# ─────────────────────────────────────────────────────────────────────────────
# 2. DML Estimator (Manual Implementation)
# ─────────────────────────────────────────────────────────────────────────────

def dml_partial_linear(panel, outcome='GDP_per_Capita', treatment='D',
                       n_splits=5, ml_method='all', seed=42):
    """Double/Debiased ML estimator for the partially linear model.

    Y = θ·D + g(X) + ε

    Uses K-fold cross-fitting to avoid overfitting bias.
    Reports θ̂, SE, t-stat, p-value, and 95% CI.

    Parameters
    ----------
    panel : DataFrame with outcome, treatment, and confounders
    outcome : str, column name for Y
    treatment : str, column name for D
    n_splits : int, number of cross-fitting folds
    ml_method : str, 'lasso', 'ridge', 'rf', 'gb', or 'all'
    seed : int, random seed

    Returns
    -------
    dict with results for each ML method
    """
    from sklearn.model_selection import KFold
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline

    # Confounders: country dummies + year trends
    country_cols = [c for c in panel.columns if c.startswith('C_')]
    X_cols = country_cols + ['Year_centered', 'Year_sq', 'Vocab_Intensity']
    X = panel[X_cols].values
    Y = panel[outcome].values
    D = panel[treatment].values

    methods = {}

    # Define ML learners
    if ml_method in ('lasso', 'all'):
        from sklearn.linear_model import LassoCV
        methods['Lasso'] = lambda: Pipeline([
            ('scaler', StandardScaler()),
            ('model', LassoCV(cv=3, max_iter=10000, random_state=seed))
        ])

    if ml_method in ('ridge', 'all'):
        from sklearn.linear_model import RidgeCV
        methods['Ridge'] = lambda: Pipeline([
            ('scaler', StandardScaler()),
            ('model', RidgeCV(cv=3))
        ])

    if ml_method in ('rf', 'all'):
        from sklearn.ensemble import RandomForestRegressor
        methods['Random Forest'] = lambda: RandomForestRegressor(
            n_estimators=200, max_depth=8, min_samples_leaf=10,
            random_state=seed, n_jobs=-1
        )

    if ml_method in ('gb', 'all'):
        from sklearn.ensemble import GradientBoostingRegressor
        methods['Gradient Boosting'] = lambda: GradientBoostingRegressor(
            n_estimators=200, max_depth=4, learning_rate=0.05,
            min_samples_leaf=10, random_state=seed
        )

    results = {}
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=seed)

    for name, make_model in methods.items():
        # Cross-fitted residuals
        resid_Y = np.zeros_like(Y, dtype=float)
        resid_D = np.zeros_like(D, dtype=float)

        for train_idx, test_idx in kf.split(X):
            X_train, X_test = X[train_idx], X[test_idx]
            Y_train, Y_test = Y[train_idx], Y[test_idx]
            D_train, D_test = D[train_idx], D[test_idx]

            # ML step 1: Y ~ X
            model_y = make_model()
            model_y.fit(X_train, Y_train)
            resid_Y[test_idx] = Y_test - model_y.predict(X_test)

            # ML step 2: D ~ X
            model_d = make_model()
            model_d.fit(X_train, D_train)
            resid_D[test_idx] = D_test - model_d.predict(X_test)

        # DML step 3: θ̂ = (ε_D' ε_D)^{-1} (ε_D' ε_Y)
        theta = np.dot(resid_D, resid_Y) / np.dot(resid_D, resid_D)

        # Neyman-orthogonal standard error
        n = len(Y)
        psi = resid_D * (resid_Y - theta * resid_D)
        var_theta = np.mean(psi ** 2) / (np.mean(resid_D ** 2) ** 2) / n
        se_theta = np.sqrt(var_theta)

        t_stat = theta / se_theta
        p_val = 2 * (1 - stats.norm.cdf(np.abs(t_stat)))
        ci_lo = theta - 1.96 * se_theta
        ci_hi = theta + 1.96 * se_theta
        sig = '***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'ns'

        results[name] = {
            'theta': theta, 'se': se_theta, 't_stat': t_stat,
            'pval': p_val, 'ci': (ci_lo, ci_hi), 'sig': sig,
            'n': n, 'resid_Y': resid_Y, 'resid_D': resid_D,
        }

    return results


# ─────────────────────────────────────────────────────────────────────────────
# 3. Sensitivity Analysis: Multiple Channels
# ─────────────────────────────────────────────────────────────────────────────

def run_channel_dml(df_gdp, df_ngram, n_splits=5):
    """Run DML for each vocabulary channel + steam placebo.

    If the water-first thesis holds:
    - Water channels should show significant θ
    - Steam should also be significant (it matters too!)
    - But water channels should show temporal precedence
    """
    print(f"\n{'='*70}")
    print("DML CHANNEL DECOMPOSITION — Continuous Treatment")
    print(f"{'='*70}")

    channel_results = {}
    for ch in ['composite', 'transport', 'power', 'canal_only', 'steam']:
        panel = build_dml_panel(df_gdp, df_ngram, channel=ch)
        if panel is None:
            print(f"\n  {ch}: SKIPPED (no vocabulary data)")
            continue

        results = dml_partial_linear(panel, n_splits=n_splits)

        channel_results[ch] = results
        print(f"\n  Channel: {ch.upper()}")
        for name, r in results.items():
            print(f"    {name:<20}  θ = {r['theta']:>8.1f}  "
                  f"(SE={r['se']:.1f})  p = {r['pval']:.4f}  {r['sig']}  "
                  f"95% CI [{r['ci'][0]:.1f}, {r['ci'][1]:.1f}]")

    print(f"{'='*70}\n")
    return channel_results


# ─────────────────────────────────────────────────────────────────────────────
# 4. Pre-Steam Subsample DML (1700-1810)
# ─────────────────────────────────────────────────────────────────────────────

def run_presteam_dml(df_gdp, df_ngram, n_splits=5):
    """DML on pre-steam subsample (1700-1810).

    This is the critical test: does the water vocabulary intensity
    predict GDP divergence BEFORE steam power dominates?
    """
    print(f"\n{'='*70}")
    print("PRE-STEAM DML (1700–1810)")
    print("Does water vocabulary predict GDP divergence before steam?")
    print(f"{'='*70}")

    # Restrict GDP to pre-steam era
    df_gdp_pre = df_gdp.loc[1700:1810]
    df_ngram_pre = df_ngram.loc[1700:1810]

    results = {}
    for ch in ['composite', 'transport', 'canal_only']:
        panel = build_dml_panel(df_gdp_pre, df_ngram_pre, channel=ch)
        if panel is None:
            continue

        r = dml_partial_linear(panel, n_splits=min(n_splits, 3))
        results[ch] = r

        print(f"\n  Channel: {ch.upper()} (1700–1810 only)")
        for name, res in r.items():
            print(f"    {name:<20}  θ = {res['theta']:>8.1f}  "
                  f"(SE={res['se']:.1f})  p = {res['pval']:.4f}  {res['sig']}")

    print(f"{'='*70}\n")
    return results


# ─────────────────────────────────────────────────────────────────────────────
# 5. DML with Mediation Structure (Water → Steam → GDP)
# ─────────────────────────────────────────────────────────────────────────────

def run_mediation_dml(df_gdp, df_ngram, n_splits=5):
    """Test the enabling hypothesis: water → steam → GDP.

    If canals enabled steam (sequential, not competing):
    1. Water vocab should predict GDP when steam is NOT controlled for
    2. Water effect should diminish when steam IS controlled for
    3. Steam effect should be large regardless

    This is consistent with mediation: water operates through steam.
    """
    print(f"\n{'='*70}")
    print("MEDIATION DML — Testing 'Water Enables Steam' Hypothesis")
    print("If canals enabled steam: water effect should diminish")
    print("when controlling for steam (mediation structure)")
    print(f"{'='*70}")

    # Build panel with BOTH water and steam treatments
    countries = [c for c in ALL_COUNTRIES if c in df_gdp.columns]

    # Compute both intensities
    agrarian = [w for w in AGRARIAN_WORDS if w in df_ngram.columns]
    industrial = [w for w in INDUSTRIAL_WORDS if w in df_ngram.columns]
    a_sum = df_ngram[agrarian].sum(axis=1)
    i_sum = df_ngram[industrial].sum(axis=1)
    water_intensity = i_sum / (a_sum + i_sum)

    steam_words = [w for w in PLACEBO_STEAM_MECH if w in df_ngram.columns]
    steam_intensity_raw = df_ngram[steam_words].sum(axis=1)
    steam_intensity = (steam_intensity_raw - steam_intensity_raw.min()) / \
                      (steam_intensity_raw.max() - steam_intensity_raw.min())

    years = df_gdp.index
    rows = []
    for year in years:
        if year not in water_intensity.index:
            continue
        w_year = float(water_intensity.loc[year])
        s_year = float(steam_intensity.loc[year])
        for c in countries:
            gdp = df_gdp.loc[year, c]
            if pd.isna(gdp):
                continue
            is_gbr = 1 if c == 'GBR' else 0
            rows.append({
                'Year': int(year),
                'Country': c,
                'GDP_per_Capita': float(gdp),
                'Treated': is_gbr,
                'D_water': w_year * is_gbr,
                'D_steam': s_year * is_gbr,
                'D_water_raw': w_year,
                'D_steam_raw': s_year,
                'Vocab_Intensity': w_year,
                'Year_centered': int(year) - 1800,
                'Year_sq': (int(year) - 1800) ** 2,
            })

    panel = pd.DataFrame(rows)
    for c_code in countries:
        panel[f'C_{c_code}'] = (panel['Country'] == c_code).astype(int)

    # Test 1: Water alone (no steam control)
    print("\n  Test 1: Water effect WITHOUT controlling for steam")
    r1 = dml_partial_linear(panel, treatment='D_water', n_splits=n_splits)
    for name, res in r1.items():
        print(f"    {name:<20}  θ_water = {res['theta']:>8.1f}  "
              f"p = {res['pval']:.4f}  {res['sig']}")

    # Test 2: Water WITH steam controlled
    # Add steam as confounder by including it in X
    panel_with_steam = panel.copy()
    # We'll run the DML but include D_steam as a confounder
    country_cols = [c for c in panel.columns if c.startswith('C_')]
    X_cols_base = country_cols + ['Year_centered', 'Year_sq', 'D_water_raw']

    print("\n  Test 2: Water effect WITH steam controlled (steam in X)")
    # Manually add steam to confounders
    panel_med = panel.copy()
    panel_med['steam_confounder'] = panel_med['D_steam']

    from sklearn.model_selection import KFold
    from sklearn.ensemble import GradientBoostingRegressor

    X_cols = [c for c in panel.columns if c.startswith('C_')] + \
             ['Year_centered', 'Year_sq', 'D_water_raw', 'D_steam']

    Y = panel['GDP_per_Capita'].values
    D = panel['D_water'].values
    X = panel[X_cols].values

    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    resid_Y = np.zeros_like(Y, dtype=float)
    resid_D = np.zeros_like(D, dtype=float)

    for train_idx, test_idx in kf.split(X):
        gb_y = GradientBoostingRegressor(n_estimators=200, max_depth=4,
                                          learning_rate=0.05, random_state=42)
        gb_y.fit(X[train_idx], Y[train_idx])
        resid_Y[test_idx] = Y[test_idx] - gb_y.predict(X[test_idx])

        gb_d = GradientBoostingRegressor(n_estimators=200, max_depth=4,
                                          learning_rate=0.05, random_state=42)
        gb_d.fit(X[train_idx], D[train_idx])
        resid_D[test_idx] = D[test_idx] - gb_d.predict(X[test_idx])

    theta_controlled = np.dot(resid_D, resid_Y) / np.dot(resid_D, resid_D)
    n = len(Y)
    psi = resid_D * (resid_Y - theta_controlled * resid_D)
    var_theta = np.mean(psi ** 2) / (np.mean(resid_D ** 2) ** 2) / n
    se = np.sqrt(var_theta)
    t_stat = theta_controlled / se
    p_val = 2 * (1 - stats.norm.cdf(np.abs(t_stat)))
    sig = '***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'ns'

    print(f"    GB (controlled)     θ_water = {theta_controlled:>8.1f}  "
          f"(SE={se:.1f})  p = {p_val:.4f}  {sig}")

    # Test 3: Steam alone
    print("\n  Test 3: Steam effect (for comparison)")
    r3 = dml_partial_linear(panel, treatment='D_steam', n_splits=n_splits)
    for name, res in r3.items():
        print(f"    {name:<20}  θ_steam = {res['theta']:>8.1f}  "
              f"p = {res['pval']:.4f}  {res['sig']}")

    # Interpretation
    water_alone = list(r1.values())[0]['theta']
    steam_alone = list(r3.values())[0]['theta']

    print(f"\n  ── MEDIATION INTERPRETATION ──")
    if abs(theta_controlled) < abs(water_alone) * 0.7:
        print(f"    Water effect DIMINISHES when steam is controlled:")
        print(f"      θ_water (alone)      = {water_alone:.1f}")
        print(f"      θ_water (controlled) = {theta_controlled:.1f}")
        pct_mediated = (1 - abs(theta_controlled) / abs(water_alone)) * 100
        print(f"    ≈ {pct_mediated:.0f}% of water's effect operates THROUGH steam")
        print(f"    → Consistent with 'water enables steam' hypothesis")
    else:
        print(f"    Water effect persists when steam is controlled:")
        print(f"      θ_water (alone)      = {water_alone:.1f}")
        print(f"      θ_water (controlled) = {theta_controlled:.1f}")
        print(f"    → Water has a DIRECT effect on GDP, not just via steam")

    print(f"{'='*70}\n")
    return {
        'water_alone': r1, 'water_controlled': theta_controlled,
        'water_controlled_se': se, 'water_controlled_p': p_val,
        'steam_alone': r3,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 6. Visualization
# ─────────────────────────────────────────────────────────────────────────────

def plot_dml_results(full_results, channel_results, presteam_results, mediation):
    """Publication-quality DML results figure."""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Double/Debiased Machine Learning — Causal Analysis',
                 fontsize=16, fontweight='bold', y=0.98)

    # ── Panel A: θ across ML methods (full sample, composite) ────────────
    ax = axes[0, 0]
    methods = list(full_results.keys())
    thetas = [full_results[m]['theta'] for m in methods]
    ses = [full_results[m]['se'] for m in methods]
    colors = ['#1a5276' if full_results[m]['pval'] < 0.05 else '#95a5a6'
              for m in methods]

    y_pos = range(len(methods))
    ax.barh(y_pos, thetas, xerr=[1.96*s for s in ses],
            color=colors, alpha=0.8, height=0.6, capsize=5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(methods, fontsize=11)
    ax.axvline(x=0, color='black', linewidth=0.8, linestyle='-')
    ax.set_xlabel('θ̂ (DML causal effect)', fontsize=11)
    ax.set_title('A — DML Estimates by ML Method\n(Composite vocabulary, full panel)',
                 fontsize=12, fontweight='bold')

    # Add p-values
    for i, m in enumerate(methods):
        p = full_results[m]['pval']
        sig = full_results[m]['sig']
        ax.text(thetas[i] + 1.96*ses[i] + 50, i,
                f'p={p:.3f} {sig}', va='center', fontsize=9)
    ax.grid(True, alpha=0.2, axis='x')

    # ── Panel B: Channel comparison ──────────────────────────────────────
    ax = axes[0, 1]
    ch_names = []
    ch_thetas = []
    ch_ses = []
    ch_pvals = []

    for ch, results in channel_results.items():
        # Use Gradient Boosting as reference
        ref = results.get('Gradient Boosting', list(results.values())[0])
        label = ch.replace('_', ' ').title()
        if ch == 'steam':
            label = 'Steam (placebo)'
        ch_names.append(label)
        ch_thetas.append(ref['theta'])
        ch_ses.append(ref['se'])
        ch_pvals.append(ref['pval'])

    y_pos = range(len(ch_names))
    colors = ['#2980b9' if p < 0.05 else '#95a5a6' for p in ch_pvals]
    # Make steam a different color
    for i, ch in enumerate(channel_results.keys()):
        if ch == 'steam':
            colors[i] = '#c0392b' if ch_pvals[i] < 0.05 else '#e6b0aa'

    ax.barh(y_pos, ch_thetas, xerr=[1.96*s for s in ch_ses],
            color=colors, alpha=0.8, height=0.6, capsize=5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(ch_names, fontsize=11)
    ax.axvline(x=0, color='black', linewidth=0.8)
    ax.set_xlabel('θ̂ (DML causal effect)', fontsize=11)
    ax.set_title('B — DML by Vocabulary Channel\n(Gradient Boosting, full panel)',
                 fontsize=12, fontweight='bold')
    for i in range(len(ch_names)):
        sig = '***' if ch_pvals[i] < 0.001 else '**' if ch_pvals[i] < 0.01 else '*' if ch_pvals[i] < 0.05 else 'ns'
        ax.text(ch_thetas[i] + 1.96*ch_ses[i] + 50, i,
                f'p={ch_pvals[i]:.3f} {sig}', va='center', fontsize=9)
    ax.grid(True, alpha=0.2, axis='x')

    # ── Panel C: Pre-steam vs Full sample ────────────────────────────────
    ax = axes[1, 0]
    comparison = []
    for ch in ['composite', 'transport', 'canal_only']:
        if ch in full_results or ch in channel_results:
            full_r = channel_results.get(ch, {})
            pre_r = presteam_results.get(ch, {})
            ref_full = full_r.get('Gradient Boosting', list(full_r.values())[0]) if full_r else None
            ref_pre = pre_r.get('Gradient Boosting', list(pre_r.values())[0]) if pre_r else None
            if ref_full and ref_pre:
                comparison.append({
                    'channel': ch.replace('_', ' ').title(),
                    'full_theta': ref_full['theta'],
                    'full_se': ref_full['se'],
                    'pre_theta': ref_pre['theta'],
                    'pre_se': ref_pre['se'],
                })

    if comparison:
        x = np.arange(len(comparison))
        width = 0.35
        full_vals = [c['full_theta'] for c in comparison]
        pre_vals = [c['pre_theta'] for c in comparison]
        full_errs = [1.96*c['full_se'] for c in comparison]
        pre_errs = [1.96*c['pre_se'] for c in comparison]

        ax.bar(x - width/2, full_vals, width, yerr=full_errs,
               label='Full (1700–1900)', color='#2980b9', alpha=0.8, capsize=5)
        ax.bar(x + width/2, pre_vals, width, yerr=pre_errs,
               label='Pre-Steam (1700–1810)', color='#e67e22', alpha=0.8, capsize=5)
        ax.set_xticks(x)
        ax.set_xticklabels([c['channel'] for c in comparison], fontsize=10)
        ax.set_ylabel('θ̂', fontsize=11)
        ax.axhline(y=0, color='black', linewidth=0.8)
        ax.legend(fontsize=9)
        ax.set_title('C — Full vs Pre-Steam DML\n(Water channels, Gradient Boosting)',
                     fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.2, axis='y')

    # ── Panel D: Mediation structure ─────────────────────────────────────
    ax = axes[1, 1]
    water_alone = list(mediation['water_alone'].values())[0]
    steam_alone = list(mediation['steam_alone'].values())[0]

    labels = ['Water\n(alone)', 'Water\n(steam controlled)', 'Steam\n(alone)']
    values = [water_alone['theta'], mediation['water_controlled'], steam_alone['theta']]
    errs = [1.96*water_alone['se'], 1.96*mediation['water_controlled_se'],
            1.96*steam_alone['se']]
    pvals = [water_alone['pval'], mediation['water_controlled_p'], steam_alone['pval']]
    bar_colors = ['#2980b9', '#85c1e9', '#c0392b']

    bars = ax.bar(range(3), values, yerr=errs, color=bar_colors,
                  alpha=0.8, capsize=5, width=0.6)
    ax.set_xticks(range(3))
    ax.set_xticklabels(labels, fontsize=10)
    ax.axhline(y=0, color='black', linewidth=0.8)
    ax.set_ylabel('θ̂', fontsize=11)
    ax.set_title('D — Mediation: Water Enables Steam?\n(Water effect with/without steam control)',
                 fontsize=12, fontweight='bold')
    for i in range(3):
        sig = '***' if pvals[i] < 0.001 else '**' if pvals[i] < 0.01 else '*' if pvals[i] < 0.05 else 'ns'
        ax.text(i, values[i] + errs[i] + 100, f'p={pvals[i]:.3f}\n{sig}',
                ha='center', fontsize=9)
    ax.grid(True, alpha=0.2, axis='y')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    out = DATA_DIR / 'dml_results.png'
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: {out}")


# ─────────────────────────────────────────────────────────────────────────────
# 7. Summary Table
# ─────────────────────────────────────────────────────────────────────────────

def print_dml_summary(full_results, channel_results, presteam_results, mediation):
    """Print publication-quality summary table."""
    print(f"\n{'='*80}")
    print("DML ANALYSIS — PUBLICATION SUMMARY TABLE")
    print(f"{'='*80}")
    print(f"\n  {'Specification':<45} {'θ̂':>8} {'SE':>8} {'p':>8} {'Sig':>5}")
    print(f"  {'-'*74}")

    # Full sample results
    print(f"  {'FULL SAMPLE (1700-1900)':<45}")
    for name, r in full_results.items():
        print(f"    {f'Composite × {name}':<43} {r['theta']:>8.1f} {r['se']:>8.1f} "
              f"{r['pval']:>8.4f} {r['sig']:>5}")

    # Channel decomposition
    print(f"\n  {'CHANNEL DECOMPOSITION (Gradient Boosting)':<45}")
    for ch, results in channel_results.items():
        ref = results.get('Gradient Boosting', list(results.values())[0])
        label = ch.replace('_', ' ').title()
        if ch == 'steam':
            label += ' (comparison)'
        print(f"    {label:<43} {ref['theta']:>8.1f} {ref['se']:>8.1f} "
              f"{ref['pval']:>8.4f} {ref['sig']:>5}")

    # Pre-steam
    print(f"\n  {'PRE-STEAM SUBSAMPLE (1700-1810)':<45}")
    for ch, results in presteam_results.items():
        ref = results.get('Gradient Boosting', list(results.values())[0])
        label = ch.replace('_', ' ').title()
        print(f"    {label:<43} {ref['theta']:>8.1f} {ref['se']:>8.1f} "
              f"{ref['pval']:>8.4f} {ref['sig']:>5}")

    # Mediation
    water_alone = list(mediation['water_alone'].values())[0]
    steam_alone = list(mediation['steam_alone'].values())[0]
    print(f"\n  {'MEDIATION ANALYSIS':<45}")
    print(f"    {'Water (alone)':<43} {water_alone['theta']:>8.1f} {water_alone['se']:>8.1f} "
          f"{water_alone['pval']:>8.4f} {water_alone['sig']:>5}")
    print(f"    {'Water (steam controlled)':<43} {mediation['water_controlled']:>8.1f} "
          f"{mediation['water_controlled_se']:>8.1f} "
          f"{mediation['water_controlled_p']:>8.4f}")
    print(f"    {'Steam (alone)':<43} {steam_alone['theta']:>8.1f} {steam_alone['se']:>8.1f} "
          f"{steam_alone['pval']:>8.4f} {steam_alone['sig']:>5}")

    if abs(mediation['water_controlled']) < abs(water_alone['theta']):
        pct = (1 - abs(mediation['water_controlled']) / abs(water_alone['theta'])) * 100
        print(f"\n  ╔══════════════════════════════════════════════════════════════╗")
        print(f"  ║  ≈{pct:.0f}% of water's GDP effect operates THROUGH steam        ║")
        print(f"  ║  → Water infrastructure as enabling precondition, not rival  ║")
        print(f"  ╚══════════════════════════════════════════════════════════════╝")

    print(f"{'='*80}\n")


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='DML Causal Analysis')
    parser.add_argument('--n-splits', type=int, default=5,
                        help='Number of cross-fitting folds')
    args = parser.parse_args()

    print('=' * 70)
    print('DOUBLE/DEBIASED MACHINE LEARNING (DML) CAUSAL ANALYSIS')
    print('Chernozhukov et al. (2018) — Continuous Treatment Intensity')
    print('=' * 70)

    # ── Load data ─────────────────────────────────────────────────────────
    print("\n── Loading data ────────────────────────────────────────────")
    df_gdp = fetch_real_maddison()
    print(f"  GDP panel: {df_gdp.shape}")

    ngram_path = DATA_DIR / 'ngram_english.csv'
    if not ngram_path.exists():
        print("  ⚠ Ngram data not found. Run fetch_data.py first.")
        return
    df_ngram = pd.read_csv(ngram_path, index_col='Year')
    print(f"  Ngram data: {df_ngram.shape}")

    # ── Full sample composite DML ─────────────────────────────────────────
    print("\n── Full Sample DML (Composite Vocabulary) ──────────────────")
    panel = build_dml_panel(df_gdp, df_ngram, channel='composite')
    print(f"  Panel: {len(panel)} obs ({panel['Country'].nunique()} countries)")
    print(f"  Treatment D range for GBR: [{panel.loc[panel['Treated']==1, 'D'].min():.3f}, "
          f"{panel.loc[panel['Treated']==1, 'D'].max():.3f}]")
    print(f"  Treatment D for controls: {panel.loc[panel['Treated']==0, 'D'].mean():.3f}")

    full_results = dml_partial_linear(panel, n_splits=args.n_splits)

    print(f"\n{'='*70}")
    print("DML RESULTS — Composite Vocabulary × GBR")
    print(f"{'='*70}")
    for name, r in full_results.items():
        print(f"\n  {name}:")
        print(f"    θ̂  = {r['theta']:.1f}  (effect of 1-unit increase in vocab intensity for GBR)")
        print(f"    SE = {r['se']:.1f}")
        print(f"    t  = {r['t_stat']:.3f}")
        print(f"    p  = {r['pval']:.6f}  {r['sig']}")
        print(f"    95% CI = [{r['ci'][0]:.1f}, {r['ci'][1]:.1f}]")
    print(f"{'='*70}")

    # ── Channel decomposition ─────────────────────────────────────────────
    print("\n── Channel Decomposition DML ────────────────────────────────")
    channel_results = run_channel_dml(df_gdp, df_ngram, n_splits=args.n_splits)

    # ── Pre-steam subsample ───────────────────────────────────────────────
    print("\n── Pre-Steam Subsample DML ──────────────────────────────────")
    presteam_results = run_presteam_dml(df_gdp, df_ngram, n_splits=args.n_splits)

    # ── Mediation analysis ────────────────────────────────────────────────
    print("\n── Mediation: Water Enables Steam ──────────────────────────")
    mediation = run_mediation_dml(df_gdp, df_ngram, n_splits=args.n_splits)

    # ── Visualization ─────────────────────────────────────────────────────
    print("\n── Generating Plots ────────────────────────────────────────")
    plot_dml_results(full_results, channel_results, presteam_results, mediation)

    # ── Summary ───────────────────────────────────────────────────────────
    print_dml_summary(full_results, channel_results, presteam_results, mediation)


if __name__ == '__main__':
    main()
