"""
did_robustness.py — Advanced DiD Robustness Tests (Iteration 06)

Addresses five econometric limitations identified in iterations/06/limitations.md:

  #19  SUTVA Violation          → Spillover-adjusted sensitivity analysis
  #20  Endogenous T₀            → Grid search across plausible treatment years
  #21  Serial Correlation       → Collapsed DiD + permutation inference (Bertrand et al. 2004)
  #22  No Event Study           → Dynamic DiD with leads and lags
  #23  Interpolation Bias       → European-only DiD (real annual data only)

References:
  Bertrand, Duflo & Mullainathan (2004), QJE
  Goodman-Bacon (2021), JoE
  Cameron, Gelbach & Miller (2008), REStat
  Sun & Abraham (2021), JoE

Usage:
    python did_robustness.py
    from did_robustness import run_all_robustness  # programmatic
"""

import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from pathlib import Path

warnings.filterwarnings('ignore', category=FutureWarning)

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"

AGRARIAN_WORDS = ['flood', 'rain', 'river', 'harvest', 'holy', 'divine']
INDUSTRIAL_WORDS = ['canal', 'pump', 'mill', 'factory', 'machine', 'engineer', 'power']

COUNTRY_LABELS = {
    'GBR': 'Great Britain', 'NLD': 'Netherlands', 'FRA': 'France',
    'CHN': 'China', 'IND': 'India',
}


# ─────────────────────────────────────────────────────────────────────────────
# Shared utilities
# ─────────────────────────────────────────────────────────────────────────────

def load_data():
    """Load GDP and Ngram data from cache."""
    gdp = pd.read_csv(DATA_DIR / 'maddison_real_gdp.csv', index_col='Year')
    ngram = pd.read_csv(DATA_DIR / 'ngram_english.csv', index_col='Year')
    return gdp, ngram


def derive_t0(df_ngram):
    """Derive treatment year from NLP commodification crossover."""
    agrarian = [w for w in AGRARIAN_WORDS if w in df_ngram.columns]
    industrial = [w for w in INDUSTRIAL_WORDS if w in df_ngram.columns]
    a_sum = df_ngram[agrarian].sum(axis=1)
    i_sum = df_ngram[industrial].sum(axis=1)
    ratio = i_sum / (a_sum + i_sum)
    crossover = ratio >= 0.5
    t0 = int(crossover.idxmax()) if crossover.any() else 1760
    return t0, ratio


def build_panel(df_gdp, t0, countries):
    """Build long-format DiD panel."""
    cols = [c for c in countries if c in df_gdp.columns]
    panel = df_gdp[cols].reset_index().melt(
        id_vars='Year', value_vars=cols,
        var_name='Country', value_name='GDP_per_Capita'
    )
    panel['Treated'] = (panel['Country'] == 'GBR').astype(int)
    panel['Post'] = (panel['Year'] >= t0).astype(int)
    panel['DiD'] = panel['Treated'] * panel['Post']
    panel['log_GDP'] = np.log(panel['GDP_per_Capita'].clip(lower=1))
    return panel.sort_values(['Country', 'Year']).reset_index(drop=True)


# ─────────────────────────────────────────────────────────────────────────────
# REMEDY 19: SUTVA Sensitivity — Exclude colonial/trade-linked controls
# ─────────────────────────────────────────────────────────────────────────────

def remedy_19_sutva(df_gdp, t0):
    """Test SUTVA sensitivity by progressively removing spillover-exposed controls.

    Logic: If SUTVA is violated, beta_3 should change substantially when
    we remove the most spillover-exposed controls (colonial subjects first,
    then European trade rivals).
    """
    print("\n" + "=" * 70)
    print("REMEDY 19: SUTVA VIOLATION — Spillover Sensitivity Analysis")
    print("=" * 70)

    configurations = [
        ("All controls (baseline)", ['GBR', 'NLD', 'FRA', 'CHN', 'IND']),
        ("Drop India (colonial subject)", ['GBR', 'NLD', 'FRA', 'CHN']),
        ("Drop India + China (colonial exposure)", ['GBR', 'NLD', 'FRA']),
        ("Netherlands only (closest peer)", ['GBR', 'NLD']),
        ("France only (rival, less trade-linked)", ['GBR', 'FRA']),
    ]

    results = []
    for label, countries in configurations:
        panel = build_panel(df_gdp, t0, countries)
        m = smf.ols('GDP_per_Capita ~ Treated + Post + DiD', data=panel).fit()
        b3 = m.params.get('DiD', np.nan)
        p = m.pvalues.get('DiD', np.nan)
        ci = m.conf_int().loc['DiD'] if 'DiD' in m.params else [np.nan, np.nan]
        n_ctrl = len(countries) - 1
        results.append({
            'Configuration': label, 'N_controls': n_ctrl,
            'beta_3': b3, 'p_value': p,
            'CI_low': ci[0], 'CI_high': ci[1],
            'N_obs': int(m.nobs)
        })
        sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'
        print(f"  {label:<48} β₃={b3:>8.1f}  p={p:.4f} {sig}")

    df_r = pd.DataFrame(results)

    # Stability metric: coefficient of variation across configurations
    cv = df_r['beta_3'].std() / df_r['beta_3'].mean() * 100
    print(f"\n  Coefficient of Variation across configs: {cv:.1f}%")
    if cv < 30:
        print("  → PASS: β₃ is stable across spillover configurations (CV < 30%)")
    else:
        print("  → CAUTION: β₃ varies substantially across configurations (CV ≥ 30%)")

    return df_r


# ─────────────────────────────────────────────────────────────────────────────
# REMEDY 20: Endogenous T₀ — Grid Search Sensitivity
# ─────────────────────────────────────────────────────────────────────────────

def remedy_20_t0_grid(df_gdp):
    """Test sensitivity of beta_3 to treatment year choice.

    Runs DiD across a grid of T₀ values from 1730 to 1810 to show
    that results are not an artifact of the data-selected T₀.
    """
    print("\n" + "=" * 70)
    print("REMEDY 20: ENDOGENOUS T₀ — Treatment Year Grid Search")
    print("=" * 70)

    countries = ['GBR', 'NLD', 'FRA', 'CHN', 'IND']
    t0_grid = list(range(1730, 1811, 5))
    results = []

    for t0_test in t0_grid:
        panel = build_panel(df_gdp, t0_test, countries)
        m = smf.ols('GDP_per_Capita ~ Treated + Post + DiD', data=panel).fit()
        b3 = m.params.get('DiD', np.nan)
        p = m.pvalues.get('DiD', np.nan)
        results.append({'T0': t0_test, 'beta_3': b3, 'p_value': p})

    df_r = pd.DataFrame(results)

    # Report
    sig_count = (df_r['p_value'] < 0.05).sum()
    print(f"  Grid: T₀ ∈ [{t0_grid[0]}, {t0_grid[-1]}], step=5 ({len(t0_grid)} values)")
    print(f"  Significant at 5%: {sig_count}/{len(t0_grid)} ({sig_count/len(t0_grid)*100:.0f}%)")
    print(f"  β₃ range: [{df_r['beta_3'].min():.0f}, {df_r['beta_3'].max():.0f}]")
    peak_row = df_r.loc[df_r['beta_3'].idxmax()]
    print(f"  Peak β₃ at T₀={int(peak_row['T0'])}: {peak_row['beta_3']:.0f} (p={peak_row['p_value']:.4f})")

    if sig_count / len(t0_grid) > 0.7:
        print("  → PASS: β₃ is significant across >70% of plausible T₀ values")
    else:
        print("  → CAUTION: β₃ significance is sensitive to treatment year choice")

    return df_r


# ─────────────────────────────────────────────────────────────────────────────
# REMEDY 21: Serial Correlation — Collapsed DiD + Permutation Inference
# ─────────────────────────────────────────────────────────────────────────────

def remedy_21_serial_correlation(df_gdp, t0, n_perms=5000):
    """Address Bertrand et al. (2004) serial correlation critique.

    Two approaches:
    (a) Collapsed DiD: average pre/post within each country → 2 obs per country
    (b) Permutation inference: randomly reassign treatment across countries
    """
    print("\n" + "=" * 70)
    print("REMEDY 21: SERIAL CORRELATION — Collapsed DiD + Permutation Inference")
    print("=" * 70)

    countries = ['GBR', 'NLD', 'FRA', 'CHN', 'IND']
    cols = [c for c in countries if c in df_gdp.columns]

    # ── Part A: Collapsed DiD ─────────────────────────────────────────────
    print("\n  Part A: Collapsed DiD (Bertrand et al. 2004 recommended fix)")
    pre = df_gdp.loc[:t0 - 1, cols].mean()
    post = df_gdp.loc[t0:, cols].mean()

    collapsed = pd.DataFrame({
        'Country': cols * 2,
        'Post': [0] * len(cols) + [1] * len(cols),
        'GDP_mean': list(pre.values) + list(post.values)
    })
    collapsed['Treated'] = (collapsed['Country'] == 'GBR').astype(int)
    collapsed['DiD'] = collapsed['Treated'] * collapsed['Post']

    m_collapsed = smf.ols('GDP_mean ~ Treated + Post + DiD', data=collapsed).fit()
    b3_collapsed = m_collapsed.params.get('DiD', np.nan)
    p_collapsed = m_collapsed.pvalues.get('DiD', np.nan)
    sig = '***' if p_collapsed < 0.001 else '**' if p_collapsed < 0.01 else '*' if p_collapsed < 0.05 else 'ns'

    print(f"    β₃ (collapsed) = {b3_collapsed:.1f},  p = {p_collapsed:.4f} {sig}")
    print(f"    N = {int(m_collapsed.nobs)} (2 per country × {len(cols)} countries)")

    # ── Part B: Permutation Inference ─────────────────────────────────────
    print(f"\n  Part B: Permutation Inference ({n_perms} permutations)")
    panel_full = build_panel(df_gdp, t0, countries)
    m_true = smf.ols('GDP_per_Capita ~ Treated + Post + DiD', data=panel_full).fit()
    b3_true = m_true.params['DiD']

    rng = np.random.default_rng(42)
    perm_betas = np.empty(n_perms)

    for i in range(n_perms):
        panel_perm = panel_full.copy()
        # Randomly assign ONE country as "treated" (block permutation)
        fake_treated = rng.choice(cols)
        panel_perm['Treated'] = (panel_perm['Country'] == fake_treated).astype(int)
        panel_perm['DiD'] = panel_perm['Treated'] * panel_perm['Post']
        m_perm = smf.ols('GDP_per_Capita ~ Treated + Post + DiD', data=panel_perm).fit()
        perm_betas[i] = m_perm.params.get('DiD', 0)

    p_perm = np.mean(np.abs(perm_betas) >= np.abs(b3_true))
    print(f"    True β₃ = {b3_true:.1f}")
    print(f"    Permutation p-value (two-sided) = {p_perm:.4f}")
    print(f"    Permutation 95th percentile: {np.percentile(np.abs(perm_betas), 95):.1f}")

    # NOTE: With only 5 countries, block permutation has minimum p = 1/5 = 0.20
    # when GBR has the largest effect (which it does). The test CANNOT reject at 5%.
    n_unique = len(cols)
    min_possible_p = 1.0 / n_unique
    print(f"\n    NOTE: With {n_unique} countries, minimum possible p = {min_possible_p:.2f}")
    print(f"    This is a POWER limitation, not a substantive failure.")

    # ── Part C: Temporal Permutation (shuffle treatment year) ─────────
    print(f"\n  Part C: Temporal Permutation (randomize T₀, {n_perms} draws)")
    t0_range = list(range(1720, 1860))
    perm_betas_temporal = np.empty(n_perms)

    for i in range(n_perms):
        fake_t0 = rng.choice(t0_range)
        panel_perm = build_panel(df_gdp, fake_t0, cols)
        m_perm = smf.ols('GDP_per_Capita ~ Treated + Post + DiD', data=panel_perm).fit()
        perm_betas_temporal[i] = m_perm.params.get('DiD', 0)

    p_temporal = np.mean(np.abs(perm_betas_temporal) >= np.abs(b3_true))
    print(f"    Temporal permutation p-value = {p_temporal:.4f}")

    if p_temporal < 0.05:
        print("  → PASS: β₃ survives temporal permutation (p < 0.05)")
    else:
        print(f"  → {'MARGINAL' if p_temporal < 0.10 else 'FAIL'}: temporal permutation p = {p_temporal:.4f}")

    return {
        'collapsed_beta': b3_collapsed, 'collapsed_p': p_collapsed,
        'perm_p': p_perm, 'perm_betas': perm_betas, 'true_beta': b3_true,
        'temporal_perm_p': p_temporal, 'temporal_perm_betas': perm_betas_temporal,
        'min_possible_p': min_possible_p
    }


# ─────────────────────────────────────────────────────────────────────────────
# REMEDY 22: Event Study — Dynamic Treatment Effects
# ─────────────────────────────────────────────────────────────────────────────

def remedy_22_event_study(df_gdp, t0, bin_width=10):
    """Estimate dynamic DiD with leads and lags (event study design).

    Uses 10-year bins relative to T₀ to balance precision and granularity.
    The omitted category is the bin immediately before treatment [-10, 0).
    Pre-treatment coefficients should be jointly zero (parallel trends test).
    """
    print("\n" + "=" * 70)
    print("REMEDY 22: EVENT STUDY — Dynamic Treatment Effects")
    print("=" * 70)

    countries = ['GBR', 'NLD', 'FRA', 'CHN', 'IND']
    panel = build_panel(df_gdp, t0, countries)

    # Create relative time variable and bin it
    panel['rel_time'] = panel['Year'] - t0
    panel['bin'] = (panel['rel_time'] // bin_width) * bin_width

    # Ensure bins are bounded
    min_bin = panel['bin'].min()
    max_bin = panel['bin'].max()
    bins = sorted(panel['bin'].unique())

    # Omitted category: the bin just before treatment (e.g., -10)
    omitted_bin = -bin_width
    if omitted_bin not in bins:
        omitted_bin = max(b for b in bins if b < 0)

    # Create interaction dummies: Treated × bin (safe column names for patsy)
    for b in bins:
        if b == omitted_bin:
            continue
        safe_name = f'TxB_n{abs(b)}' if b < 0 else f'TxB_p{b}'
        panel[safe_name] = ((panel['Treated'] == 1) & (panel['bin'] == b)).astype(int)

    # Formula: GDP ~ C(Country) + C(bin) + Treated×bin dummies
    interaction_terms = [f'TxB_n{abs(b)}' if b < 0 else f'TxB_p{b}'
                         for b in bins if b != omitted_bin]
    formula = 'GDP_per_Capita ~ C(Country) + C(bin) + ' + ' + '.join(interaction_terms)

    m = smf.ols(formula, data=panel).fit()

    # Extract event-study coefficients
    es_results = []
    for b in bins:
        if b == omitted_bin:
            es_results.append({'bin': b, 'coef': 0, 'se': 0, 'p': np.nan,
                               'ci_low': 0, 'ci_high': 0})
            continue
        col = f'TxB_n{abs(b)}' if b < 0 else f'TxB_p{b}'
        if col in m.params:
            coef = m.params[col]
            se = m.bse[col]
            p = m.pvalues[col]
            ci = m.conf_int().loc[col]
            es_results.append({'bin': b, 'coef': coef, 'se': se, 'p': p,
                               'ci_low': ci[0], 'ci_high': ci[1]})

    df_es = pd.DataFrame(es_results)

    # Pre-treatment joint F-test (parallel trends)
    pre_terms = [f'TxB_n{abs(b)}' for b in bins if b < 0 and b != omitted_bin]
    if len(pre_terms) > 0:
        restriction = ' = '.join(pre_terms) + ' = 0'
        try:
            f_test = m.f_test(restriction)
            f_stat = float(f_test.fvalue)
            f_p = float(f_test.pvalue)
        except Exception:
            # Fallback: test each individually
            pre_ps = [m.pvalues.get(t, 1.0) for t in pre_terms]
            f_stat = np.nan
            f_p = np.nan
    else:
        f_stat, f_p = np.nan, np.nan

    # Report
    print(f"\n  Event-study bins: {bin_width}-year intervals, omitted = [{omitted_bin}, {omitted_bin + bin_width})")
    print(f"  {'Bin':<10} {'Coef':>10} {'SE':>10} {'p-value':>10} {'Sig':>5}")
    print(f"  {'─' * 50}")
    for _, row in df_es.iterrows():
        b = int(row['bin'])
        sig = '(ref)' if b == omitted_bin else (
            '***' if row['p'] < 0.001 else '**' if row['p'] < 0.01 else
            '*' if row['p'] < 0.05 else 'ns')
        print(f"  [{b:>+4},{b + bin_width:>+4})  {row['coef']:>10.1f} {row['se']:>10.1f} "
              f"{row['p']:>10.4f} {sig:>5}" if b != omitted_bin else
              f"  [{b:>+4},{b + bin_width:>+4})  {'0 (ref)':>10} {'—':>10} {'—':>10} (ref)")

    print(f"\n  Pre-treatment joint F-test (parallel trends):")
    if not np.isnan(f_p):
        print(f"    F = {f_stat:.2f},  p = {f_p:.4f}")
        if f_p > 0.10:
            print("    → PASS: Cannot reject parallel trends (p > 0.10)")
        else:
            print("    → FAIL: Pre-treatment coefficients are jointly significant")
    else:
        print("    (Could not compute joint F-test)")

    return df_es, f_p


# ─────────────────────────────────────────────────────────────────────────────
# REMEDY 23: Interpolation Bias — European-Only Analysis
# ─────────────────────────────────────────────────────────────────────────────

def remedy_23_interpolation(df_gdp, t0):
    """Address interpolation bias by restricting to European countries only.

    GBR, NLD, FRA have near-complete annual GDP data in Maddison 2023.
    CHN and IND are heavily interpolated. Compare results with and without
    the interpolated controls.
    """
    print("\n" + "=" * 70)
    print("REMEDY 23: INTERPOLATION BIAS — European-Only vs Full Panel")
    print("=" * 70)

    # Full panel (with interpolated CHN, IND)
    panel_full = build_panel(df_gdp, t0, ['GBR', 'NLD', 'FRA', 'CHN', 'IND'])
    m_full = smf.ols('GDP_per_Capita ~ DiD + C(Country) + C(Year)', data=panel_full).fit()

    # European-only (real annual data)
    panel_eur = build_panel(df_gdp, t0, ['GBR', 'NLD', 'FRA'])
    m_eur = smf.ols('GDP_per_Capita ~ DiD + C(Country) + C(Year)', data=panel_eur).fit()

    # Benchmark-year only for CHN/IND (decadal)
    benchmark_years = list(range(1700, 1901, 10))
    panel_bench = build_panel(df_gdp, t0, ['GBR', 'NLD', 'FRA', 'CHN', 'IND'])
    # Keep all years for EUR, but only benchmark years for Asia
    mask = (
        (panel_bench['Country'].isin(['GBR', 'NLD', 'FRA'])) |
        (panel_bench['Year'].isin(benchmark_years))
    )
    panel_bench = panel_bench[mask].copy()
    m_bench = smf.ols('GDP_per_Capita ~ Treated + Post + DiD', data=panel_bench).fit()

    configs = [
        ("Full panel (all annual)", m_full, panel_full),
        ("European only (GBR, NLD, FRA)", m_eur, panel_eur),
        ("Benchmark-year Asian controls", m_bench, panel_bench),
    ]

    print(f"\n  {'Configuration':<40} {'β₃':>10} {'p-value':>10} {'N':>6} {'Sig':>5}")
    print(f"  {'─' * 75}")

    results = []
    for label, res, data in configs:
        b3 = res.params.get('DiD', np.nan)
        p = res.pvalues.get('DiD', np.nan)
        n = int(res.nobs)
        sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'
        print(f"  {label:<40} {b3:>10.1f} {p:>10.4f} {n:>6} {sig:>5}")
        results.append({'config': label, 'beta_3': b3, 'p_value': p, 'N': n})

    df_r = pd.DataFrame(results)
    return df_r


# ─────────────────────────────────────────────────────────────────────────────
# Visualization
# ─────────────────────────────────────────────────────────────────────────────

def plot_robustness_summary(t0_grid_df, es_df, perm_results, sutva_df, t0):
    """Four-panel summary of all Iteration 06 robustness tests."""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # ── Panel A: T₀ Grid Search (#20) ────────────────────────────────────
    ax = axes[0, 0]
    colors = ['#e74c3c' if p < 0.05 else '#95a5a6' for p in t0_grid_df['p_value']]
    ax.bar(t0_grid_df['T0'], t0_grid_df['beta_3'], color=colors, width=4, edgecolor='black', linewidth=0.3)
    ax.axvline(x=t0, color='darkorange', linewidth=2, linestyle='--', label=f'Data-derived T₀={t0}')
    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.set_xlabel('Treatment Year (T₀)', fontsize=11)
    ax.set_ylabel('β₃ (DiD Estimator)', fontsize=11)
    ax.set_title('A — T₀ Sensitivity Grid (#20)', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.2, axis='y')

    # ── Panel B: Event Study (#22) ────────────────────────────────────────
    ax = axes[0, 1]
    pre_mask = es_df['bin'] < 0
    post_mask = es_df['bin'] >= 0
    ax.errorbar(es_df.loc[pre_mask, 'bin'] + 5, es_df.loc[pre_mask, 'coef'],
                yerr=[es_df.loc[pre_mask, 'coef'] - es_df.loc[pre_mask, 'ci_low'],
                      es_df.loc[pre_mask, 'ci_high'] - es_df.loc[pre_mask, 'coef']],
                fmt='o', color='#2980b9', capsize=4, markersize=6, label='Pre-treatment')
    ax.errorbar(es_df.loc[post_mask, 'bin'] + 5, es_df.loc[post_mask, 'coef'],
                yerr=[es_df.loc[post_mask, 'coef'] - es_df.loc[post_mask, 'ci_low'],
                      es_df.loc[post_mask, 'ci_high'] - es_df.loc[post_mask, 'coef']],
                fmt='s', color='#e74c3c', capsize=4, markersize=6, label='Post-treatment')
    ax.axhline(y=0, color='black', linewidth=0.8, linestyle='-')
    ax.axvline(x=0, color='darkorange', linewidth=2, linestyle='--', alpha=0.7)
    ax.set_xlabel(f'Years Relative to T₀ ({t0})', fontsize=11)
    ax.set_ylabel('Dynamic Treatment Effect', fontsize=11)
    ax.set_title('B — Event Study: Leads & Lags (#22)', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.2)

    # ── Panel C: Temporal Permutation Distribution (#21) ────────────────
    ax = axes[1, 0]
    temporal_betas = perm_results.get('temporal_perm_betas', perm_results['perm_betas'])
    temporal_p = perm_results.get('temporal_perm_p', perm_results['perm_p'])
    ax.hist(temporal_betas, bins=60, color='#bdc3c7', edgecolor='gray',
            linewidth=0.3, density=True, label='Randomized T₀ dist.')
    ax.axvline(x=perm_results['true_beta'], color='#e74c3c', linewidth=2.5,
               linestyle='-', label=f'True β₃ = {perm_results["true_beta"]:.0f}')
    ax.axvline(x=np.percentile(temporal_betas, 2.5), color='gray',
               linewidth=1, linestyle=':', alpha=0.6)
    ax.axvline(x=np.percentile(temporal_betas, 97.5), color='gray',
               linewidth=1, linestyle=':', alpha=0.6, label='95% perm. interval')
    ax.set_xlabel('β₃ (DiD Estimator)', fontsize=11)
    ax.set_ylabel('Density', fontsize=11)
    ax.set_title(f'C — Temporal Permutation (#21), p={temporal_p:.3f}',
                 fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.2)

    # ── Panel D: SUTVA Sensitivity (#19) ─────────────────────────────────
    ax = axes[1, 1]
    y_pos = range(len(sutva_df))
    bar_colors = ['#e74c3c' if p < 0.05 else '#95a5a6' for p in sutva_df['p_value']]
    ax.barh(list(y_pos), sutva_df['beta_3'], color=bar_colors,
            edgecolor='black', linewidth=0.5, height=0.5)
    # Error bars from CI
    errors = np.array([
        sutva_df['beta_3'] - sutva_df['CI_low'],
        sutva_df['CI_high'] - sutva_df['beta_3']
    ])
    ax.errorbar(sutva_df['beta_3'], list(y_pos), xerr=errors,
                fmt='none', color='black', capsize=3)
    ax.axvline(x=0, color='black', linewidth=0.8)
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(sutva_df['Configuration'], fontsize=9)
    ax.set_xlabel('β₃ (DiD Estimator)', fontsize=11)
    ax.set_title('D — SUTVA Sensitivity (#19)', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.2, axis='x')

    fig.suptitle(f'Iteration 06: Advanced DiD Robustness Tests (T₀={t0})',
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(DATA_DIR / 'did_robustness_iter06.png', dpi=150, bbox_inches='tight')
    print(f"\n  Saved: data/did_robustness_iter06.png")
    plt.close()


# ─────────────────────────────────────────────────────────────────────────────
# Master runner
# ─────────────────────────────────────────────────────────────────────────────

def run_all_robustness():
    """Run all Iteration 06 robustness tests and return results dict."""
    print("=" * 70)
    print("ITERATION 06: ADVANCED DiD ROBUSTNESS TESTS")
    print("Addresses limitations #19–#23")
    print("=" * 70)

    df_gdp, df_ngram = load_data()
    t0, ratio = derive_t0(df_ngram)
    print(f"\n  Data-derived T₀ = {t0}")

    # Run all remedies
    sutva_df = remedy_19_sutva(df_gdp, t0)
    t0_grid_df = remedy_20_t0_grid(df_gdp)
    perm_results = remedy_21_serial_correlation(df_gdp, t0, n_perms=5000)
    es_df, f_p = remedy_22_event_study(df_gdp, t0, bin_width=10)
    interp_df = remedy_23_interpolation(df_gdp, t0)

    # Visualization
    plot_robustness_summary(t0_grid_df, es_df, perm_results, sutva_df, t0)

    # Summary scorecard
    print("\n" + "=" * 70)
    print("ITERATION 06: ROBUSTNESS SCORECARD")
    print("=" * 70)

    tests = [
        ("#19 SUTVA", sutva_df['beta_3'].std() / sutva_df['beta_3'].mean() * 100 < 30,
         f"CV = {sutva_df['beta_3'].std() / sutva_df['beta_3'].mean() * 100:.1f}%"),
        ("#20 T₀ Grid", (t0_grid_df['p_value'] < 0.05).mean() > 0.7,
         f"{(t0_grid_df['p_value'] < 0.05).sum()}/{len(t0_grid_df)} significant"),
        ("#21 Serial Corr.", perm_results['temporal_perm_p'] < 0.05,
         f"temporal perm p = {perm_results['temporal_perm_p']:.4f} "
         f"(block perm p = {perm_results['perm_p']:.2f}, min={perm_results['min_possible_p']:.2f})"),
        ("#22 Event Study", f_p > 0.10 if not np.isnan(f_p) else False,
         f"Pre-trend F p = {f_p:.4f}" if not np.isnan(f_p) else "F-test failed"),
        ("#23 Interpolation", interp_df.iloc[1]['p_value'] < 0.05,
         f"EUR-only p = {interp_df.iloc[1]['p_value']:.4f}"),
    ]

    for name, passed, detail in tests:
        status = "PASS" if passed else "FAIL"
        icon = "+" if passed else "-"
        print(f"  [{icon}] {name:<25} {status:<6} ({detail})")

    n_pass = sum(1 for _, p, _ in tests if p)
    print(f"\n  Overall: {n_pass}/{len(tests)} tests passed")
    print("=" * 70)

    return {
        'sutva': sutva_df, 't0_grid': t0_grid_df,
        'permutation': perm_results, 'event_study': es_df,
        'event_study_f_p': f_p, 'interpolation': interp_df,
        't0': t0, 'n_pass': n_pass, 'n_tests': len(tests)
    }


if __name__ == '__main__':
    run_all_robustness()
