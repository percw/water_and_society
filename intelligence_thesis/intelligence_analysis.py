"""
intelligence_analysis.py — The Intelligence Commodification Thesis

"Are We at 1760?" — Testing whether the linguistic commodification of
intelligence follows the same pattern as water's 18th-century shift.

Phases:
  1. Ngram trajectories + commodification ratio + crossover detection
  2. Granger causality: linguistic shift -> GDP divergence
  3. Onset timing analysis (the key test)
  4. DiD: AI-adopting vs non-adopting economies
  5. Comparison with water thesis pattern

References:
  Michel et al. (2011), Science — Culturomics
  Brynjolfsson & McAfee (2014), The Second Machine Age
  Acemoglu & Restrepo (2020), Robots and Jobs
"""

import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from scipy import stats
from pathlib import Path

warnings.filterwarnings('ignore')

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"

from fetch_intelligence_data import (
    SACRED_WORDS, COMMODITY_WORDS, COMMODITY_BIGRAMS,
    fetch_ngram_data, fetch_gdp_data
)

ALL_COMMODITY = COMMODITY_WORDS + COMMODITY_BIGRAMS


def vocab_sum(df, words):
    available = [w for w in words if w in df.columns]
    return df[available].sum(axis=1) if available else pd.Series(0, index=df.index)


def smooth(s, window=5):
    return s.rolling(window, center=True, min_periods=1).mean()


def normalize(s):
    r = s - s.min()
    mx = r.max()
    return r / mx if mx > 0 else r


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 1: Ngram Trajectories + Commodification Ratio
# ─────────────────────────────────────────────────────────────────────────────

def phase_1_trajectories(df_ngram):
    """Plot vocabulary trajectories and compute commodification ratio."""
    print("\n" + "=" * 70)
    print("PHASE 1: NGRAM TRAJECTORIES — Sacred vs Commodity Intelligence")
    print("=" * 70)

    sacred_sum = smooth(vocab_sum(df_ngram, SACRED_WORDS))
    commodity_sum = smooth(vocab_sum(df_ngram, ALL_COMMODITY))
    total = sacred_sum + commodity_sum
    ratio = commodity_sum / total.clip(lower=1e-15)

    # Find crossover
    crossover_mask = ratio >= 0.5
    if crossover_mask.any():
        crossover_year = int(crossover_mask.idxmax())
    else:
        crossover_year = None

    print(f"  Sacred sum (1950): {sacred_sum.iloc[0]:.2e}")
    print(f"  Sacred sum (2019): {sacred_sum.iloc[-1]:.2e}")
    print(f"  Commodity sum (1950): {commodity_sum.iloc[0]:.2e}")
    print(f"  Commodity sum (2019): {commodity_sum.iloc[-1]:.2e}")
    print(f"  Ratio 1950: {ratio.iloc[0]:.3f}")
    print(f"  Ratio 2019: {ratio.iloc[-1]:.3f}")
    print(f"  CROSSOVER YEAR: {crossover_year}")

    return sacred_sum, commodity_sum, ratio, crossover_year


def phase_1_plot(df_ngram, sacred_sum, commodity_sum, ratio, crossover_year):
    """Three-panel Phase 1 visualization."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Panel A: Individual word trajectories
    ax = axes[0]
    colors_s = plt.cm.Blues(np.linspace(0.3, 0.9, len(SACRED_WORDS)))
    colors_c = plt.cm.Reds(np.linspace(0.3, 0.9, len(ALL_COMMODITY)))
    for i, w in enumerate(SACRED_WORDS):
        if w in df_ngram.columns:
            ax.plot(df_ngram.index, smooth(df_ngram[w]), color=colors_s[i],
                    linewidth=1, alpha=0.7, label=w if i < 5 else None)
    for i, w in enumerate(ALL_COMMODITY):
        if w in df_ngram.columns:
            ax.plot(df_ngram.index, smooth(df_ngram[w]), color=colors_c[i],
                    linewidth=1, alpha=0.7, linestyle='--',
                    label=w if i < 5 else None)
    ax.set_xlabel('Year')
    ax.set_ylabel('Ngram Frequency')
    ax.set_title('A - Individual Word Trajectories', fontweight='bold')
    ax.legend(fontsize=7, ncol=2, loc='upper left')
    ax.grid(True, alpha=0.2)

    # Panel B: Aggregate Sacred vs Commodity
    ax = axes[1]
    ax.fill_between(sacred_sum.index, 0, sacred_sum, alpha=0.3, color='#2980b9',
                    label='Sacred/Human')
    ax.fill_between(commodity_sum.index, 0, commodity_sum, alpha=0.3, color='#e74c3c',
                    label='Commodity/Machine')
    ax.plot(sacred_sum.index, sacred_sum, color='#2980b9', linewidth=2)
    ax.plot(commodity_sum.index, commodity_sum, color='#e74c3c', linewidth=2)
    if crossover_year:
        ax.axvline(x=crossover_year, color='darkorange', linewidth=2, linestyle='--')
        ax.annotate(f'Crossover\n{crossover_year}', xy=(crossover_year, sacred_sum.max() * 0.5),
                    fontsize=10, fontweight='bold', color='darkorange')
    ax.set_xlabel('Year')
    ax.set_ylabel('Aggregate Frequency')
    ax.set_title('B - Sacred vs Commodity Intelligence', fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.2)

    # Panel C: Commodification Ratio
    ax = axes[2]
    ax.plot(ratio.index, ratio, color='purple', linewidth=2)
    ax.axhline(y=0.5, color='gray', linestyle=':', alpha=0.6)
    if crossover_year:
        ax.axvline(x=crossover_year, color='darkorange', linewidth=2, linestyle='--')
    ax.fill_between(ratio.index, ratio, 0.5,
                    where=ratio > 0.5, alpha=0.15, color='red', label='Machine > Human')
    ax.fill_between(ratio.index, ratio, 0.5,
                    where=ratio <= 0.5, alpha=0.15, color='blue', label='Human > Machine')
    ax.set_xlabel('Year')
    ax.set_ylabel('Commodification Ratio')
    ax.set_title('C - Intelligence Commodification Ratio', fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.2)

    fig.suptitle('Phase 1: The Linguistic Commodification of Intelligence (1950-2019)',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(DATA_DIR / 'phase1_intelligence_trajectories.png', dpi=150, bbox_inches='tight')
    print(f"  Saved: phase1_intelligence_trajectories.png")
    plt.close()


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 2: Granger Causality + GDP Overlay
# ─────────────────────────────────────────────────────────────────────────────

def phase_2_granger(df_ngram, df_gdp, crossover_year):
    """Test whether intelligence commodification Granger-causes GDP divergence."""
    print("\n" + "=" * 70)
    print("PHASE 2: GRANGER CAUSALITY — Linguistic Shift -> GDP")
    print("=" * 70)

    from statsmodels.tsa.stattools import grangercausalitytests

    commodity_sum = smooth(vocab_sum(df_ngram, ALL_COMMODITY))
    sacred_sum = smooth(vocab_sum(df_ngram, SACRED_WORDS))

    results = {}
    for country in ['USA', 'DEU', 'FRA', 'ITA', 'KOR', 'JPN']:
        if country not in df_gdp.columns:
            continue
        gdp = df_gdp[country]
        common = commodity_sum.index.intersection(gdp.index)
        if len(common) < 20:
            continue

        # First differences for stationarity
        d_gdp = gdp.loc[common].diff().dropna()
        d_comm = commodity_sum.loc[common].diff().dropna()
        common2 = d_gdp.index.intersection(d_comm.index)
        data = pd.DataFrame({'GDP': d_gdp.loc[common2], 'Commodity': d_comm.loc[common2]}).dropna()

        if len(data) < 15:
            continue

        try:
            gc = grangercausalitytests(data[['GDP', 'Commodity']], maxlag=5, verbose=False)
            best_lag = min(gc.keys(), key=lambda k: gc[k][0]['ssr_ftest'][1])
            p = gc[best_lag][0]['ssr_ftest'][1]
            f_stat = gc[best_lag][0]['ssr_ftest'][0]
            sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'
            print(f"  {country}: Commodity vocab -> GDP: F={f_stat:.2f}, p={p:.4f} {sig} (lag={best_lag})")
            results[country] = {'p': p, 'f': f_stat, 'lag': best_lag}
        except Exception as e:
            print(f"  {country}: Error ({e})")

    return results


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 3: Onset Timing Analysis (Key Test)
# ─────────────────────────────────────────────────────────────────────────────

def phase_3_onset(df_ngram, df_gdp):
    """Replicate the water thesis onset timing analysis.

    When did:
    1. Commodity vocabulary accelerate?
    2. USA GDP diverge from European average?
    3. Comparison with water thesis timing lag.
    """
    print("\n" + "=" * 70)
    print("PHASE 3: ONSET TIMING — Are We at 1760?")
    print("=" * 70)

    commodity_sum = smooth(vocab_sum(df_ngram, ALL_COMMODITY))
    sacred_sum = smooth(vocab_sum(df_ngram, SACRED_WORDS))

    # Vocab acceleration onset (above 75th percentile of growth rate)
    comm_growth = commodity_sum.diff().rolling(5, center=True, min_periods=3).mean()
    comm_accel = comm_growth[comm_growth > comm_growth.quantile(0.75)]
    comm_onset = int(comm_accel.index[0]) if len(comm_accel) > 0 else None

    # Sacred deceleration (when growth goes negative)
    sacred_growth = sacred_sum.diff().rolling(5, center=True, min_periods=3).mean()
    sacred_decline = sacred_growth[sacred_growth < 0]
    sacred_onset = int(sacred_decline.index[0]) if len(sacred_decline) > 0 else None

    # USA GDP divergence from European average
    eur_avg = df_gdp[['DEU', 'FRA', 'ITA']].mean(axis=1)
    ratio = df_gdp['USA'] / eur_avg
    ratio_smooth = ratio.rolling(5, center=True, min_periods=3).mean()
    # When does USA pull away? Already ahead, so look for acceleration
    ratio_growth = ratio_smooth.diff().rolling(5, center=True, min_periods=3).mean()
    # Find sustained positive divergence acceleration
    div_accel = ratio_growth[ratio_growth > ratio_growth.quantile(0.75)]
    div_onset = int(div_accel.index[0]) if len(div_accel) > 0 else None

    # Compute USA absolute divergence (gap)
    gap = df_gdp['USA'] - eur_avg
    gap_growth = gap.diff().rolling(5, center=True, min_periods=3).mean()
    gap_accel = gap_growth[gap_growth > gap_growth.quantile(0.8)]
    gap_onset = int(gap_accel.index[0]) if len(gap_accel) > 0 else None

    print(f"  Commodity vocab acceleration onset: {comm_onset}")
    print(f"  Sacred vocab decline onset: {sacred_onset}")
    print(f"  USA/EUR ratio acceleration: {div_onset}")
    print(f"  USA-EUR gap acceleration: {gap_onset}")

    if comm_onset and gap_onset:
        lead = gap_onset - comm_onset
        print(f"\n  Commodity vocab leads GDP gap acceleration by: {lead} years")
    else:
        lead = None

    # Compare with water thesis
    print(f"\n  COMPARISON WITH WATER THESIS:")
    print(f"  Water:        vocab accel 1760 -> GDP diverge 1804 -> fossil accel 1817  (44y lead)")
    if comm_onset and gap_onset:
        print(f"  Intelligence: vocab accel {comm_onset} -> GDP gap accel {gap_onset}  ({lead}y lead)")
        if 15 <= abs(lead) <= 60:
            print(f"  -> CONSISTENT: Lead time ({lead}y) is in the same order as water ({44}y)")
        elif lead > 0:
            print(f"  -> PLAUSIBLE: Positive lead, though different magnitude")
        else:
            print(f"  -> INCONSISTENT: Vocab does not lead GDP")

    return {
        'commodity_onset': comm_onset, 'sacred_decline': sacred_onset,
        'div_onset': div_onset, 'gap_onset': gap_onset, 'lead': lead
    }


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 4: DiD — AI-Adopting vs Non-Adopting Economies
# ─────────────────────────────────────────────────────────────────────────────

def phase_4_did(df_gdp, t0):
    """DiD with USA as treatment, European economies as controls."""
    print("\n" + "=" * 70)
    print(f"PHASE 4: DIFFERENCE-IN-DIFFERENCES (T0={t0})")
    print("=" * 70)

    countries = ['USA', 'DEU', 'FRA', 'ITA']
    cols = [c for c in countries if c in df_gdp.columns]

    panel = df_gdp[cols].reset_index().melt(
        id_vars='Year', value_vars=cols,
        var_name='Country', value_name='GDP_pc'
    )
    panel['Treated'] = (panel['Country'] == 'USA').astype(int)
    panel['Post'] = (panel['Year'] >= t0).astype(int)
    panel['DiD'] = panel['Treated'] * panel['Post']

    # Baseline
    m1 = smf.ols('GDP_pc ~ Treated + Post + DiD', data=panel).fit()
    b3 = m1.params.get('DiD', np.nan)
    p = m1.pvalues.get('DiD', np.nan)
    sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'
    print(f"\n  Baseline DiD: beta3={b3:.0f}, p={p:.4f} {sig}")

    # Two-way FE
    m2 = smf.ols('GDP_pc ~ DiD + C(Country) + C(Year)', data=panel).fit()
    b3_fe = m2.params.get('DiD', np.nan)
    p_fe = m2.pvalues.get('DiD', np.nan)
    sig_fe = '***' if p_fe < 0.001 else '**' if p_fe < 0.01 else '*' if p_fe < 0.05 else 'ns'
    print(f"  Two-way FE:   beta3={b3_fe:.0f}, p={p_fe:.4f} {sig_fe}")

    # T0 grid search
    print(f"\n  T0 Grid Search:")
    grid_results = []
    for t0_test in range(1960, 2011, 5):
        p_test = panel.copy()
        p_test['Post'] = (p_test['Year'] >= t0_test).astype(int)
        p_test['DiD'] = p_test['Treated'] * p_test['Post']
        m = smf.ols('GDP_pc ~ Treated + Post + DiD', data=p_test).fit()
        grid_results.append({
            'T0': t0_test, 'beta3': m.params.get('DiD', np.nan),
            'p': m.pvalues.get('DiD', np.nan)
        })
    df_grid = pd.DataFrame(grid_results)
    peak = df_grid.loc[df_grid['beta3'].abs().idxmax()]
    sig_count = (df_grid['p'] < 0.05).sum()
    print(f"    Significant at 5%: {sig_count}/{len(df_grid)}")
    print(f"    Peak beta3 at T0={int(peak['T0'])}: {peak['beta3']:.0f}")

    return {
        'baseline_beta': b3, 'baseline_p': p,
        'twfe_beta': b3_fe, 'twfe_p': p_fe,
        'grid': df_grid
    }


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 5: Master Visualization
# ─────────────────────────────────────────────────────────────────────────────

def plot_master(df_ngram, df_gdp, sacred_sum, commodity_sum, ratio,
                crossover_year, onset_results, did_results):
    """Four-panel master visualization."""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # Panel A: Commodification ratio with crossover
    ax = axes[0, 0]
    ax.plot(ratio.index, ratio, color='purple', linewidth=2.5)
    ax.axhline(y=0.5, color='gray', linestyle=':', alpha=0.6)
    if crossover_year:
        ax.axvline(x=crossover_year, color='darkorange', linewidth=2, linestyle='--')
        ax.annotate(f'Crossover\n{crossover_year}', xy=(crossover_year, 0.55),
                    fontsize=11, fontweight='bold', color='darkorange')
    ax.fill_between(ratio.index, ratio, 0.5,
                    where=ratio > 0.5, alpha=0.15, color='red')
    ax.fill_between(ratio.index, ratio, 0.5,
                    where=ratio <= 0.5, alpha=0.15, color='blue')
    ax.set_ylabel('Commodity / (Sacred + Commodity)')
    ax.set_title('A - Intelligence Commodification Crossover', fontweight='bold', fontsize=13)
    ax.grid(True, alpha=0.2)

    # Panel B: GDP trajectories
    ax = axes[0, 1]
    colors = {'USA': '#1a5276', 'DEU': '#8e44ad', 'FRA': '#2980b9',
              'ITA': '#27ae60', 'KOR': '#e74c3c', 'JPN': '#f39c12',
              'BRA': '#95a5a6', 'IND': '#d35400', 'NGA': '#7f8c8d'}
    for c in ['USA', 'DEU', 'FRA', 'ITA', 'KOR', 'JPN']:
        if c in df_gdp.columns:
            lw = 3 if c == 'USA' else 1.5
            ax.plot(df_gdp.index, df_gdp[c], color=colors.get(c, 'gray'),
                    linewidth=lw, label=c)
    if crossover_year:
        ax.axvline(x=crossover_year, color='darkorange', linewidth=2, linestyle='--')
    ax.set_ylabel('GDP per capita (2017 PPP $)')
    ax.set_title('B - GDP Trajectories: AI Adopters', fontweight='bold', fontsize=13)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.2)

    # Panel C: Onset timeline
    ax = axes[1, 0]
    events = []
    if onset_results.get('commodity_onset'):
        events.append(('Machine Vocab\nAcceleration', onset_results['commodity_onset'], '#e74c3c'))
    if onset_results.get('sacred_decline'):
        events.append(('Human Vocab\nDecline', onset_results['sacred_decline'], '#2980b9'))
    if onset_results.get('gap_onset'):
        events.append(('USA-EUR Gap\nAcceleration', onset_results['gap_onset'], '#27ae60'))

    events.sort(key=lambda x: x[1])
    for i, (label, year, color) in enumerate(events):
        ax.barh(i, year - 1945, left=1945, color=color, height=0.5,
                edgecolor='black', linewidth=0.5)
        ax.text(year + 1, i, f'{year}', va='center', fontsize=12, fontweight='bold')
        ax.text(1947, i, label, va='center', fontsize=10, color=color, fontweight='bold')

    ax.set_xlim(1945, 2025)
    ax.set_yticks([])
    ax.set_xlabel('Year')
    ax.set_title('C - Onset Timeline: Who Came First?', fontweight='bold', fontsize=13)
    ax.grid(True, alpha=0.2, axis='x')

    if onset_results.get('lead'):
        ax.text(0.5, -0.12, f"Vocab leads GDP gap acceleration by {onset_results['lead']} years",
                transform=ax.transAxes, ha='center', fontsize=12,
                fontweight='bold', style='italic')

    # Panel D: DiD T0 grid
    ax = axes[1, 1]
    grid = did_results['grid']
    bar_colors = ['#e74c3c' if p < 0.05 else '#95a5a6' for p in grid['p']]
    ax.bar(grid['T0'], grid['beta3'], color=bar_colors, width=4,
           edgecolor='black', linewidth=0.3)
    if crossover_year:
        ax.axvline(x=crossover_year, color='darkorange', linewidth=2, linestyle='--',
                   label=f'Crossover T0={crossover_year}')
    ax.axhline(y=0, color='black', linewidth=0.8)
    ax.set_xlabel('Treatment Year (T0)')
    ax.set_ylabel('DiD beta3')
    ax.set_title('D - DiD Sensitivity to T0', fontweight='bold', fontsize=13)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.2, axis='y')

    fig.suptitle('The Intelligence Commodification Thesis: "Are We at 1760?"',
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(DATA_DIR / 'intelligence_master.png', dpi=150, bbox_inches='tight')
    print(f"\n  Saved: intelligence_master.png")
    plt.close()


# ─────────────────────────────────────────────────────────────────────────────
# Master Runner
# ─────────────────────────────────────────────────────────────────────────────

def run_intelligence_thesis():
    """Run the complete Intelligence Commodification analysis."""
    print("=" * 70)
    print("THE INTELLIGENCE COMMODIFICATION THESIS")
    print('"Are We at 1760?"')
    print("=" * 70)

    df_ngram = fetch_ngram_data()
    df_gdp = fetch_gdp_data()

    # Phase 1
    sacred_sum, commodity_sum, ratio, crossover_year = phase_1_trajectories(df_ngram)
    phase_1_plot(df_ngram, sacred_sum, commodity_sum, ratio, crossover_year)

    # Phase 2
    granger_results = phase_2_granger(df_ngram, df_gdp, crossover_year)

    # Phase 3 (Key Test)
    onset_results = phase_3_onset(df_ngram, df_gdp)

    # Phase 4
    t0 = crossover_year or 1995
    did_results = phase_4_did(df_gdp, t0)

    # Master viz
    plot_master(df_ngram, df_gdp, sacred_sum, commodity_sum, ratio,
                crossover_year, onset_results, did_results)

    # ── Final Scorecard ──────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("INTELLIGENCE THESIS: SCORECARD")
    print("=" * 70)

    tests = [
        ("Commodification crossover detected", crossover_year is not None,
         f"Year: {crossover_year}" if crossover_year else "No crossover"),
        ("Sacred vocab declining", sacred_sum.iloc[-1] < sacred_sum.iloc[0],
         f"{sacred_sum.iloc[0]:.2e} -> {sacred_sum.iloc[-1]:.2e}"),
        ("Commodity vocab rising", commodity_sum.iloc[-1] > commodity_sum.iloc[0] * 5,
         f"{commodity_sum.iloc[0]:.2e} -> {commodity_sum.iloc[-1]:.2e}"),
        ("Vocab leads GDP gap",
         onset_results.get('lead') is not None and onset_results['lead'] > 0,
         f"{onset_results.get('lead', '?')} years" if onset_results.get('lead') else "N/A"),
        ("DiD USA vs EUR significant",
         did_results['baseline_p'] < 0.05,
         f"p={did_results['baseline_p']:.4f}"),
        ("Pattern matches water thesis",
         crossover_year is not None and onset_results.get('lead', 0) and onset_results['lead'] > 10,
         f"Crossover {crossover_year}, lead {onset_results.get('lead', '?')}y (water: 1760, 44y)"),
    ]

    for name, passed, detail in tests:
        icon = "+" if passed else "-"
        status = "PASS" if passed else "FAIL"
        print(f"  [{icon}] {name:<45} {status:<6} ({detail})")

    n_pass = sum(1 for _, p, _ in tests if p)
    print(f"\n  Overall: {n_pass}/{len(tests)} tests passed")

    if n_pass >= 5:
        print("\n  CONCLUSION: STRONG support for the Intelligence Commodification Thesis")
        print("  The pattern matches the water thesis. We ARE at 1760.")
    elif n_pass >= 3:
        print("\n  CONCLUSION: MODERATE support — the linguistic shift is real,")
        print("  but the GDP prediction is still forming.")
    else:
        print("\n  CONCLUSION: WEAK — insufficient evidence for the pattern.")

    print("=" * 70)
    return {
        'crossover_year': crossover_year,
        'onset': onset_results,
        'did': did_results,
        'granger': granger_results,
        'n_pass': n_pass
    }


if __name__ == '__main__':
    run_intelligence_thesis()
