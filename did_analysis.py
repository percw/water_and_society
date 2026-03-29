"""
did_analysis.py — Difference-in-Differences (DiD) Causal Analysis (v2)

Tests whether Great Britain's GDP divergence is causally attributable
to the hydro-social linguistic shift, using a full econometric DiD
framework with multiple robustness specifications.

Data:   Maddison Project Database 2023 (real download from Dataverse)
        Google Books Ngram Corpus (for treatment year derivation)

Treatment Group:   Great Britain (GBR)
Control Groups:    Netherlands (NLD), France (FRA), China (CHN), India (IND)

Robustness specifications:
    1. Baseline DiD (pooled OLS)
    2. Year fixed effects
    3. Country fixed effects
    4. Two-way FE (country + year)
    5. Log-GDP specification
    6. HAC / Newey-West standard errors
    7. European-only controls (NLD + FRA)
    8. Asian-only controls (CHN + IND)
    9. Placebo test (fake T₀)

Usage:
    python did_analysis.py            # Full analysis with real data
    python did_analysis.py --t0 1760  # Override treatment year

References:
    Angrist & Pischke (2009), "Mostly Harmless Econometrics"
    Bolt & van Zanden (2024), Maddison Project Database 2023
"""

import argparse
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import statsmodels.formula.api as smf
from pathlib import Path

warnings.filterwarnings('ignore', category=FutureWarning)

# ── Paths ────────────────────────────────────────────────────────────────────
PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"

# ── Vocabulary (mirrors fetch_data.py) ───────────────────────────────────────
AGRARIAN_WORDS = ['flood', 'rain', 'river', 'harvest', 'holy', 'divine']
INDUSTRIAL_WORDS = ['canal', 'pump', 'mill', 'factory', 'machine', 'engineer', 'power']

# Countries
TREATMENT = ['GBR']
CONTROLS_EUR = ['NLD', 'FRA']
CONTROLS_ASIA = ['CHN', 'IND']
ALL_COUNTRIES = TREATMENT + CONTROLS_EUR + CONTROLS_ASIA

COUNTRY_LABELS = {
    'GBR': 'Great Britain', 'NLD': 'Netherlands', 'FRA': 'France',
    'CHN': 'China', 'IND': 'India',
}


# ─────────────────────────────────────────────────────────────────────────────
# 1. Data Acquisition — Real Maddison Download
# ─────────────────────────────────────────────────────────────────────────────

def fetch_real_maddison(force=False):
    """Download the real Maddison Project Database 2023 from Dataverse.

    Returns DataFrame with annual GDP per capita for all countries.
    GBR, NLD, FRA have near-complete annual data (1500-1900).
    CHN, IND are interpolated from sparse benchmarks.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    cache = DATA_DIR / 'maddison_real_gdp.csv'

    if cache.exists() and not force:
        df = pd.read_csv(cache, index_col='Year')
        print(f"  Loaded cached real Maddison: {df.shape}")
        return df

    print("  Downloading Maddison 2023 from Dataverse...")
    try:
        import requests
        from io import BytesIO
        import openpyxl

        url = 'https://dataverse.nl/api/access/datafile/421302'
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()

        df_full = pd.read_excel(BytesIO(resp.content), sheet_name='Full data')
        df_full.columns = [str(c).strip().lower() for c in df_full.columns]

        frames = {}
        for code in ALL_COUNTRIES:
            mask = ((df_full['countrycode'] == code) &
                    (df_full['year'] >= 1500) & (df_full['year'] <= 1900))
            sub = df_full.loc[mask, ['year', 'gdppc']].dropna(subset=['gdppc'])
            s = sub.set_index('year')['gdppc']
            # Reindex to full range and interpolate gaps
            s = s.reindex(range(1500, 1901))
            n_real = s.notna().sum()
            s = s.interpolate(method='linear').ffill().bfill()
            frames[code] = s
            print(f"    {code}: {n_real} real observations → {len(s)} annual (interpolated)")

        df = pd.DataFrame(frames)
        df.index.name = 'Year'
        # Trim to 1700-1900 for our analysis window
        df = df.loc[1700:1900]
        df.to_csv(cache)
        print(f"  ✓ Saved real Maddison data: {df.shape}")
        return df

    except Exception as e:
        print(f"  ⚠ Download failed: {e}")
        print("  Falling back to fetch_data.py embedded data...")
        from fetch_data import fetch_maddison
        return fetch_maddison()


# ─────────────────────────────────────────────────────────────────────────────
# 2. Derive T₀ from NLP Data
# ─────────────────────────────────────────────────────────────────────────────

def derive_treatment_year(df_ngram):
    """Find the year where the commodification ratio first crosses 0.5."""
    agrarian = [w for w in AGRARIAN_WORDS if w in df_ngram.columns]
    industrial = [w for w in INDUSTRIAL_WORDS if w in df_ngram.columns]

    a_sum = df_ngram[agrarian].sum(axis=1)
    i_sum = df_ngram[industrial].sum(axis=1)
    ratio = i_sum / (a_sum + i_sum)

    crossover = ratio >= 0.5
    t0 = int(crossover.idxmax()) if crossover.any() else 1760

    print(f"\n{'='*60}")
    print("TREATMENT YEAR DERIVATION (NLP Commodification Crossover)")
    print(f"{'='*60}")
    print(f"  Ratio at 1700: {ratio.iloc[0]:.3f}  →  1800: {ratio.loc[1800]:.3f}  →  1900: {ratio.iloc[-1]:.3f}")
    print(f"  ➤ Crossover year T₀ = {t0}")
    print(f"{'='*60}\n")
    return t0, ratio


# ─────────────────────────────────────────────────────────────────────────────
# 3. Build Panel Data
# ─────────────────────────────────────────────────────────────────────────────

def build_panel(df_gdp, t0, countries=None):
    """Melt GDP to long panel format with DiD dummy variables."""
    countries = countries or [c for c in ALL_COUNTRIES if c in df_gdp.columns]

    panel = df_gdp[countries].reset_index().melt(
        id_vars='Year', value_vars=countries,
        var_name='Country', value_name='GDP_per_Capita'
    )
    panel['Treated'] = (panel['Country'] == 'GBR').astype(int)
    panel['Post'] = (panel['Year'] >= t0).astype(int)
    panel['DiD_Interaction'] = panel['Treated'] * panel['Post']
    panel['log_GDP'] = np.log(panel['GDP_per_Capita'].clip(lower=1))

    return panel.sort_values(['Country', 'Year']).reset_index(drop=True)


# ─────────────────────────────────────────────────────────────────────────────
# 4. Multi-Specification DiD Regressions
# ─────────────────────────────────────────────────────────────────────────────

def run_all_specifications(panel, panel_eur, panel_asia, t0):
    """Run all DiD specifications and return results table."""
    specs = []

    # ── Spec 1: Baseline pooled OLS (all countries) ───────────────────────
    m1 = smf.ols('GDP_per_Capita ~ Treated + Post + DiD_Interaction',
                 data=panel).fit()
    specs.append(('1. Baseline (all)', m1, panel))

    # ── Spec 2: Year fixed effects ────────────────────────────────────────
    m2 = smf.ols('GDP_per_Capita ~ Treated + DiD_Interaction + C(Year)',
                 data=panel).fit()
    specs.append(('2. Year FE', m2, panel))

    # ── Spec 3: Country fixed effects ─────────────────────────────────────
    m3 = smf.ols('GDP_per_Capita ~ Post + DiD_Interaction + C(Country)',
                 data=panel).fit()
    specs.append(('3. Country FE', m3, panel))

    # ── Spec 4: Two-way FE (country + year) ──────────────────────────────
    m4 = smf.ols('GDP_per_Capita ~ DiD_Interaction + C(Country) + C(Year)',
                 data=panel).fit()
    specs.append(('4. Two-way FE', m4, panel))

    # ── Spec 5: Log-GDP ──────────────────────────────────────────────────
    m5 = smf.ols('log_GDP ~ Treated + Post + DiD_Interaction',
                 data=panel).fit()
    specs.append(('5. Log GDP', m5, panel))

    # ── Spec 6: HAC / Newey-West standard errors ─────────────────────────
    m6 = smf.ols('GDP_per_Capita ~ Treated + Post + DiD_Interaction',
                 data=panel).fit(cov_type='HAC',
                                 cov_kwds={'maxlags': 10})
    specs.append(('6. Newey-West HAC', m6, panel))

    # ── Spec 7: European controls only (NLD + FRA) ───────────────────────
    m7 = smf.ols('GDP_per_Capita ~ Treated + Post + DiD_Interaction',
                 data=panel_eur).fit()
    specs.append(('7. European controls', m7, panel_eur))

    # ── Spec 8: Asian controls only (CHN + IND) ──────────────────────────
    m8 = smf.ols('GDP_per_Capita ~ Treated + Post + DiD_Interaction',
                 data=panel_asia).fit()
    specs.append(('8. Asian controls', m8, panel_asia))

    # ── Spec 9: Placebo test (T₀ shifted 50 years early) ─────────────────
    fake_t0 = t0 - 50
    panel_placebo = panel.copy()
    panel_placebo['Post'] = (panel_placebo['Year'] >= fake_t0).astype(int)
    panel_placebo['DiD_Interaction'] = panel_placebo['Treated'] * panel_placebo['Post']
    # Only use pre-treatment data to test for false positive
    panel_placebo = panel_placebo[panel_placebo['Year'] < t0]
    m9 = smf.ols('GDP_per_Capita ~ Treated + Post + DiD_Interaction',
                 data=panel_placebo).fit()
    specs.append((f'9. Placebo T₀={fake_t0}', m9, panel_placebo))

    return specs


def print_specification_table(specs):
    """Print a clean comparison table of all specifications."""
    print(f"\n{'='*90}")
    print("MULTI-SPECIFICATION DiD RESULTS — ROBUSTNESS TABLE")
    print(f"{'='*90}")
    print(f"{'Specification':<26} {'β₃ (DiD)':>10} {'Std Err':>10} {'t-stat':>8} "
          f"{'p-value':>10} {'R²':>8} {'N':>6} {'Sig':>5}")
    print(f"{'─'*90}")

    for name, res, data in specs:
        b3 = res.params.get('DiD_Interaction', np.nan)
        se = res.bse.get('DiD_Interaction', np.nan)
        t = res.tvalues.get('DiD_Interaction', np.nan)
        p = res.pvalues.get('DiD_Interaction', np.nan)
        r2 = res.rsquared
        n = int(res.nobs)
        sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'

        # For log spec, show as percentage
        if 'Log' in name:
            print(f"{name:<26} {b3:>10.4f} {se:>10.4f} {t:>8.2f} "
                  f"{p:>10.4f} {r2:>8.4f} {n:>6} {sig:>5}")
        else:
            print(f"{name:<26} {b3:>10.1f} {se:>10.1f} {t:>8.2f} "
                  f"{p:>10.4f} {r2:>8.4f} {n:>6} {sig:>5}")

    print(f"{'─'*90}")
    print("Significance: *** p<0.001, ** p<0.01, * p<0.05, ns = not significant")
    print(f"{'='*90}\n")


# ─────────────────────────────────────────────────────────────────────────────
# 5. Visualizations
# ─────────────────────────────────────────────────────────────────────────────

def plot_parallel_trends(df_gdp, t0, ratio=None):
    """Multi-panel parallel trends plot with real data annotations."""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    colors = {'GBR': '#1a5276', 'NLD': '#8e44ad', 'FRA': '#2980b9',
              'CHN': '#c0392b', 'IND': '#27ae60'}
    styles = {'GBR': '-', 'NLD': '--', 'FRA': '-.', 'CHN': ':', 'IND': ':'}

    # ── Panel A: All countries full period ─────────────────────────────────
    ax = axes[0, 0]
    for c in ALL_COUNTRIES:
        if c in df_gdp.columns:
            ax.plot(df_gdp.index, df_gdp[c], color=colors[c],
                    linewidth=2.5 if c == 'GBR' else 1.5,
                    linestyle=styles[c], label=COUNTRY_LABELS.get(c, c))
    ax.axvline(x=t0, color='darkorange', linewidth=2, linestyle=':', zorder=5)
    ax.annotate(f'T₀={t0}', xy=(t0, df_gdp['GBR'].max() * 0.6),
                fontsize=11, fontweight='bold', color='darkorange')
    ax.axvspan(df_gdp.index.min(), t0, alpha=0.03, color='green')
    ax.axvspan(t0, df_gdp.index.max(), alpha=0.03, color='red')
    ax.set_ylabel('GDP/capita (2011 int\'l $)', fontsize=11)
    ax.set_title('A — All Countries: Full Period', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9, framealpha=0.9)
    ax.grid(True, alpha=0.2)

    # ── Panel B: European comparison (GBR vs NLD, FRA) ─────────────────────
    ax = axes[0, 1]
    for c in ['GBR', 'NLD', 'FRA']:
        if c in df_gdp.columns:
            ax.plot(df_gdp.index, df_gdp[c], color=colors[c],
                    linewidth=2.5 if c == 'GBR' else 1.8,
                    linestyle=styles[c], label=COUNTRY_LABELS.get(c, c))
    ax.axvline(x=t0, color='darkorange', linewidth=2, linestyle=':', zorder=5)
    ax.axvspan(df_gdp.index.min(), t0, alpha=0.03, color='green')
    ax.axvspan(t0, df_gdp.index.max(), alpha=0.03, color='red')
    ax.set_ylabel('GDP/capita (2011 int\'l $)', fontsize=11)
    ax.set_title('B — European Controls (NLD, FRA) — Real Annual Data',
                 fontsize=13, fontweight='bold')
    ax.legend(fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.2)

    # ── Panel C: Pre-treatment zoom (parallel trends test) ─────────────────
    ax = axes[1, 0]
    pre = df_gdp.loc[:t0-1]
    for c in ALL_COUNTRIES:
        if c in pre.columns:
            # Index to base year = 100 for slope comparison
            indexed = (pre[c] / pre[c].iloc[0]) * 100
            ax.plot(pre.index, indexed, color=colors[c],
                    linewidth=2.5 if c == 'GBR' else 1.5,
                    linestyle=styles[c], label=COUNTRY_LABELS.get(c, c))
    ax.axhline(y=100, color='gray', linewidth=0.8, linestyle=':')
    ax.set_ylabel('Indexed GDP (1700 = 100)', fontsize=11)
    ax.set_xlabel('Year', fontsize=11)
    ax.set_title(f'C — Pre-Treatment Trends (1700–{t0-1}), Indexed',
                 fontsize=13, fontweight='bold')
    ax.legend(fontsize=9, framealpha=0.9)
    ax.grid(True, alpha=0.2)

    # ── Panel D: NLP Commodification Ratio ─────────────────────────────────
    ax = axes[1, 1]
    if ratio is not None:
        ax.plot(ratio.index, ratio, color='purple', linewidth=2)
        ax.axhline(y=0.5, color='gray', linestyle=':', alpha=0.6)
        ax.axvline(x=t0, color='darkorange', linewidth=2, linestyle=':')
        ax.fill_between(ratio.index, ratio, 0.5,
                        where=ratio > 0.5, alpha=0.15, color='red',
                        label='Industrial > Agrarian')
        ax.fill_between(ratio.index, ratio, 0.5,
                        where=ratio <= 0.5, alpha=0.15, color='green',
                        label='Agrarian > Industrial')
        ax.set_ylabel('Commodification Ratio', fontsize=11)
        ax.set_title('D — NLP Crossover Point (Treatment Derivation)',
                     fontsize=13, fontweight='bold')
        ax.legend(fontsize=9, framealpha=0.9, loc='lower right')
    else:
        ax.text(0.5, 0.5, '(Ngram data unavailable)', transform=ax.transAxes,
                ha='center', fontsize=14, color='gray')
    ax.set_xlabel('Year', fontsize=11)
    ax.grid(True, alpha=0.2)

    fig.suptitle(f'Difference-in-Differences: Parallel Trends Validation (T₀={t0})',
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(DATA_DIR / 'did_parallel_trends.png', dpi=150, bbox_inches='tight')
    print("  ✓ Saved: data/did_parallel_trends.png")
    plt.close()


def plot_specification_comparison(specs, t0):
    """Bar chart comparing β₃ across all specifications."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # Separate log spec from level specs
    level_specs = [(n, r, d) for n, r, d in specs if 'Log' not in n]
    log_specs = [(n, r, d) for n, r, d in specs if 'Log' in n]

    # ── Panel A: Level specifications ─────────────────────────────────────
    ax = axes[0]
    names = [n for n, _, _ in level_specs]
    betas = [r.params.get('DiD_Interaction', 0) for _, r, _ in level_specs]
    ci_low = [r.conf_int().loc['DiD_Interaction', 0] if 'DiD_Interaction' in r.params
              else 0 for _, r, _ in level_specs]
    ci_high = [r.conf_int().loc['DiD_Interaction', 1] if 'DiD_Interaction' in r.params
               else 0 for _, r, _ in level_specs]
    pvals = [r.pvalues.get('DiD_Interaction', 1) for _, r, _ in level_specs]

    errors = np.array([[b - lo for b, lo in zip(betas, ci_low)],
                       [hi - b for b, hi in zip(betas, ci_high)]])

    bar_colors = ['#e74c3c' if p < 0.05 else '#95a5a6' for p in pvals]
    bars = ax.barh(range(len(names)), betas, xerr=errors, color=bar_colors,
                   edgecolor='black', linewidth=0.5, capsize=4, height=0.55)
    ax.axvline(x=0, color='black', linewidth=0.8)

    for i, (b, p) in enumerate(zip(betas, pvals)):
        stars = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'
        ax.text(max(b + errors[1][i], 0) + 80, i,
                f' {b:.0f} ({stars})', va='center', fontsize=9,
                fontweight='bold' if p < 0.05 else 'normal')

    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=10)
    ax.set_xlabel('β₃ DiD Estimator (GDP per capita)', fontsize=11)
    ax.set_title('A — β₃ Across Specifications (Level)', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.2, axis='x')

    # ── Panel B: 2×2 DiD decomposition (baseline) ─────────────────────────
    ax2 = axes[1]
    base_res = specs[0][1]  # baseline specification
    intercept = base_res.params['Intercept']
    b1 = base_res.params['Treated']
    b2 = base_res.params['Post']
    b3 = base_res.params['DiD_Interaction']

    control_pre = intercept
    control_post = intercept + b2
    treated_pre = intercept + b1
    treated_post = intercept + b1 + b2 + b3
    counterfactual = intercept + b1 + b2

    x_pos = [0, 1]
    ax2.plot(x_pos, [control_pre, control_post], 'o-', color='#c0392b',
             linewidth=2, markersize=10, label='Controls (avg)')
    ax2.plot(x_pos, [treated_pre, treated_post], 's-', color='#1a5276',
             linewidth=2.5, markersize=12, label='GBR (Treatment)')
    ax2.plot(x_pos, [treated_pre, counterfactual], 's:', color='#1a5276',
             linewidth=1.5, markersize=8, alpha=0.35,
             label='GBR counterfactual')

    ax2.annotate('', xy=(1.08, treated_post), xytext=(1.08, counterfactual),
                 arrowprops=dict(arrowstyle='<->', color='darkorange', lw=2.5))
    ax2.text(1.15, (treated_post + counterfactual) / 2,
             f'β₃ = {b3:.0f}\n(DiD effect)', fontsize=11,
             fontweight='bold', color='darkorange', va='center')

    ax2.set_xticks(x_pos)
    ax2.set_xticklabels([f'Pre-Shift\n(before {t0})', f'Post-Shift\n(≥ {t0})'],
                        fontsize=11)
    ax2.set_ylabel('Mean GDP/capita (2011 int\'l $)', fontsize=11)
    ax2.set_title('B — DiD 2×2 Decomposition (Baseline)', fontsize=13,
                  fontweight='bold')
    ax2.legend(fontsize=10, framealpha=0.9)
    ax2.grid(True, alpha=0.2)
    ax2.set_xlim(-0.3, 1.55)

    fig.suptitle(f'DiD Robustness: β₃ Stability Across Specifications (T₀={t0})',
                 fontsize=15, fontweight='bold')
    plt.tight_layout()
    plt.savefig(DATA_DIR / 'did_regression_results.png', dpi=150, bbox_inches='tight')
    print("  ✓ Saved: data/did_regression_results.png")
    plt.close()


# ─────────────────────────────────────────────────────────────────────────────
# 6. Full Baseline Summary
# ─────────────────────────────────────────────────────────────────────────────

def print_baseline_detail(specs):
    """Print the full OLS summary for the baseline and two-way FE specs."""
    for name, res, _ in specs:
        if name in ('1. Baseline (all)', '4. Two-way FE', '7. European controls'):
            print(f"\n{'='*60}")
            print(f"FULL RESULTS — {name}")
            print(f"{'='*60}")
            print(res.summary())

            if 'DiD_Interaction' in res.params:
                b3 = res.params['DiD_Interaction']
                p = res.pvalues['DiD_Interaction']
                ci = res.conf_int().loc['DiD_Interaction']
                print(f"\n  β₃ = {b3:.1f},  p = {p:.6f},  95% CI = [{ci[0]:.1f}, {ci[1]:.1f}]")
                if p < 0.05 and b3 > 0:
                    print(f"  ✓ SIGNIFICANT: Britain gained ~{b3:.0f} extra GDP/capita from the hydro-social shift")
                else:
                    print(f"  ○ Not significant at 5% level")


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='DiD causal analysis — hydro-social shift → GDP divergence')
    parser.add_argument('--t0', type=int, default=None,
                        help='Override treatment year')
    parser.add_argument('--force', action='store_true',
                        help='Re-download data')
    args = parser.parse_args()

    print('=' * 60)
    print('DIFFERENCE-IN-DIFFERENCES (DiD) CAUSAL ANALYSIS v2')
    print('Real Maddison Data + Multi-Specification Robustness')
    print('=' * 60)

    # ── Load real data ────────────────────────────────────────────────────
    df_gdp = fetch_real_maddison(force=args.force)
    print(f"  GDP panel: {df_gdp.shape[0]} years × {df_gdp.shape[1]} countries")
    print(f"  Countries: {df_gdp.columns.tolist()}")

    # ── Derive T₀ ────────────────────────────────────────────────────────
    ratio = None
    ngram_path = DATA_DIR / 'ngram_english.csv'
    if args.t0:
        t0 = args.t0
        print(f"\n  Using manually specified T₀ = {t0}")
    elif ngram_path.exists():
        df_ngram = pd.read_csv(ngram_path, index_col='Year')
        t0, ratio = derive_treatment_year(df_ngram)
    else:
        t0 = 1760
        print(f"\n  ⚠ Ngram data not found; using default T₀ = {t0}")

    # ── Build panels ──────────────────────────────────────────────────────
    print("\n── Building Panel Data ──────────────────────────────────────")
    panel_all = build_panel(df_gdp, t0, ['GBR'] + CONTROLS_EUR + CONTROLS_ASIA)
    panel_eur = build_panel(df_gdp, t0, ['GBR'] + CONTROLS_EUR)
    panel_asia = build_panel(df_gdp, t0, ['GBR'] + CONTROLS_ASIA)

    print(f"  All controls:      {len(panel_all)} obs ({panel_all['Country'].nunique()} countries)")
    print(f"  European controls: {len(panel_eur)} obs ({panel_eur['Country'].nunique()} countries)")
    print(f"  Asian controls:    {len(panel_asia)} obs ({panel_asia['Country'].nunique()} countries)")

    # ── Parallel trends ───────────────────────────────────────────────────
    print("\n── Parallel Trends ─────────────────────────────────────────")
    plot_parallel_trends(df_gdp, t0, ratio)

    # ── Multi-specification regressions ───────────────────────────────────
    print("\n── Running 9 DiD Specifications ─────────────────────────────")
    specs = run_all_specifications(panel_all, panel_eur, panel_asia, t0)
    print_specification_table(specs)
    print_baseline_detail(specs)

    # ── Specification comparison chart ────────────────────────────────────
    plot_specification_comparison(specs, t0)

    print(f"\n{'='*60}")
    print("DiD analysis v2 complete. Outputs saved to data/")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
