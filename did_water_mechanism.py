"""
did_water_mechanism.py — Water-Specific Mechanism DiD (Iteration 07)

Addresses the Attribution Gap (#24): the standard DiD proves Britain diverged
but cannot pin it to water specifically.

Key insight: the thesis is about TIMING not MAGNITUDE. Water doesn't need
a bigger total effect than fossil — it needs an EARLIER effect. The strategies
therefore test temporal precedence within the DiD framework.

Strategies:
  1. Sequential Period Decomposition — split divergence into water-era and
     fossil-era components
  2. Lagged Intensity DiD — does LAGGED water predict GDP before lagged fossil?
  3. First-Difference Horse Race — in growth rates, which leads?
  4. Cross-Correlation Timing — formal lead/lag structure
  5. Placebo Vocabulary Tournament — competing vocabs as controls

References:
  Callaway & Sant'Anna (2021), JoE
  Angrist & Pischke (2009), Ch. 5
  Granger (1969), Econometrica
"""

import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import statsmodels.api as sm
from scipy import stats
from pathlib import Path

warnings.filterwarnings('ignore')

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"

AGRARIAN_WORDS = ['flood', 'rain', 'river', 'harvest', 'holy', 'divine']
INDUSTRIAL_WORDS = ['canal', 'pump', 'mill', 'factory', 'machine', 'engineer', 'power']

# Unambiguous water infrastructure bigrams
WATER_INFRA = ['water wheel', 'water mill', 'water power', 'water frame',
               'water engine', 'mill race', 'overshot', 'undershot',
               'breast wheel', 'inland navigation', 'canal navigation']

FOSSIL_TERMS = ['steam', 'coal', 'engine']
RELIGIOUS_WORDS = ['holy', 'divine']
AGRARIAN_ONLY = ['flood', 'rain', 'harvest']

ALL_COUNTRIES = ['GBR', 'NLD', 'FRA', 'CHN', 'IND']
EUR_COUNTRIES = ['GBR', 'NLD', 'FRA']


def load_data():
    gdp = pd.read_csv(DATA_DIR / 'maddison_real_gdp.csv', index_col='Year')
    ngram = pd.read_csv(DATA_DIR / 'ngram_english.csv', index_col='Year')
    return gdp, ngram


def vocab_intensity(df_ngram, words):
    available = [w for w in words if w in df_ngram.columns]
    if not available:
        return pd.Series(0, index=df_ngram.index)
    raw = df_ngram[available].sum(axis=1)
    return raw.rolling(5, center=True, min_periods=1).mean()


def normalize(s):
    r = s - s.min()
    mx = r.max()
    return r / mx if mx > 0 else r


# ─────────────────────────────────────────────────────────────────────────────
# STRATEGY 1: Sequential Period Decomposition
# ─────────────────────────────────────────────────────────────────────────────

def strategy_1_sequential_periods(df_gdp, df_ngram):
    """Split the Great Divergence into water-era and fossil-era.

    1700-1810: Water should explain GBR divergence from European controls
    1810-1900: Fossil should take over

    This tests the first-mover thesis directly: water started the divergence,
    fossil accelerated it.
    """
    print("\n" + "=" * 70)
    print("STRATEGY 1: SEQUENTIAL PERIOD DECOMPOSITION")
    print("Water-era (1700-1810) vs Fossil-era (1810-1900)")
    print("=" * 70)

    results = {}

    for period_label, yr_start, yr_end in [
        ('Water Era (1700-1810)', 1700, 1810),
        ('Fossil Era (1810-1900)', 1810, 1900),
        ('Full Period (1700-1900)', 1700, 1900),
    ]:
        gdp_sub = df_gdp.loc[yr_start:yr_end]
        ngram_sub = df_ngram.loc[yr_start:yr_end]

        water = normalize(vocab_intensity(ngram_sub, WATER_INFRA))
        fossil = normalize(vocab_intensity(ngram_sub, FOSSIL_TERMS))
        gbr_gdp = gdp_sub['GBR']

        # Granger-style: does lagged vocab predict GDP growth?
        # Use first differences to ensure stationarity
        d_gdp = gbr_gdp.diff().dropna()
        d_water = water.diff().dropna()
        d_fossil = fossil.diff().dropna()

        # Align
        common = d_gdp.index.intersection(d_water.index).intersection(d_fossil.index)
        if len(common) < 15:
            results[period_label] = {'water_r': np.nan, 'fossil_r': np.nan}
            continue

        dg = d_gdp.loc[common].values
        dw = d_water.loc[common].values
        df_ = d_fossil.loc[common].values

        # Correlation of GDP growth with lagged vocab growth (lag=10 years)
        lag = 10
        if len(common) > lag + 10:
            r_water, p_water = stats.pearsonr(dg[lag:], dw[:-lag])
            r_fossil, p_fossil = stats.pearsonr(dg[lag:], df_[:-lag])
        else:
            r_water, p_water = stats.pearsonr(dg, dw)
            r_fossil, p_fossil = stats.pearsonr(dg, df_)

        results[period_label] = {
            'water_r': r_water, 'water_p': p_water,
            'fossil_r': r_fossil, 'fossil_p': p_fossil,
            'n': len(common)
        }

        w_sig = '***' if p_water < 0.001 else '**' if p_water < 0.01 else '*' if p_water < 0.05 else 'ns'
        f_sig = '***' if p_fossil < 0.001 else '**' if p_fossil < 0.01 else '*' if p_fossil < 0.05 else 'ns'
        winner = 'WATER' if abs(r_water) > abs(r_fossil) and p_water < 0.10 else \
                 'FOSSIL' if abs(r_fossil) > abs(r_water) and p_fossil < 0.10 else 'NEITHER'

        print(f"\n  {period_label} (N={len(common)}):")
        print(f"    Water growth -> GDP growth (lag={lag}y): r={r_water:.3f}, p={p_water:.4f} {w_sig}")
        print(f"    Fossil growth -> GDP growth (lag={lag}y): r={r_fossil:.3f}, p={p_fossil:.4f} {f_sig}")
        print(f"    Winner: {winner}")

    return results


# ─────────────────────────────────────────────────────────────────────────────
# STRATEGY 2: Cross-Correlation Timing Test
# ─────────────────────────────────────────────────────────────────────────────

def strategy_2_cross_correlation(df_gdp, df_ngram):
    """Compute cross-correlation between vocabulary growth and GDP growth.

    At which lag does each vocabulary most strongly predict GDP?
    Water should peak at an EARLIER lag than fossil.
    """
    print("\n" + "=" * 70)
    print("STRATEGY 2: CROSS-CORRELATION TIMING TEST")
    print("At which lag does each vocab best predict GDP growth?")
    print("=" * 70)

    gbr_gdp = df_gdp['GBR']
    water = normalize(vocab_intensity(df_ngram, WATER_INFRA))
    fossil = normalize(vocab_intensity(df_ngram, FOSSIL_TERMS))

    # First differences
    dg = gbr_gdp.diff().dropna()
    dw = water.diff().dropna()
    df_ = fossil.diff().dropna()
    common = dg.index.intersection(dw.index).intersection(df_.index)
    dg = dg.loc[common]; dw = dw.loc[common]; df_ = df_.loc[common]

    max_lag = 30
    results = {'lag': [], 'water_r': [], 'fossil_r': [], 'water_p': [], 'fossil_p': []}

    for lag in range(1, max_lag + 1):
        if len(common) <= lag + 5:
            break
        r_w, p_w = stats.pearsonr(dg.values[lag:], dw.values[:-lag])
        r_f, p_f = stats.pearsonr(dg.values[lag:], df_.values[:-lag])
        results['lag'].append(lag)
        results['water_r'].append(r_w)
        results['fossil_r'].append(r_f)
        results['water_p'].append(p_w)
        results['fossil_p'].append(p_f)

    df_cc = pd.DataFrame(results)

    # Find peak correlation lag for each
    water_peak_idx = df_cc['water_r'].abs().idxmax()
    fossil_peak_idx = df_cc['fossil_r'].abs().idxmax()
    water_peak = df_cc.loc[water_peak_idx]
    fossil_peak = df_cc.loc[fossil_peak_idx]

    print(f"\n  Water peak: lag={int(water_peak['lag'])}y, r={water_peak['water_r']:.3f}, p={water_peak['water_p']:.4f}")
    print(f"  Fossil peak: lag={int(fossil_peak['lag'])}y, r={fossil_peak['fossil_r']:.3f}, p={fossil_peak['fossil_p']:.4f}")

    # Find first significant lag for each
    water_first_sig = df_cc[df_cc['water_p'] < 0.10]
    fossil_first_sig = df_cc[df_cc['fossil_p'] < 0.10]

    w_first = int(water_first_sig.iloc[0]['lag']) if len(water_first_sig) > 0 else None
    f_first = int(fossil_first_sig.iloc[0]['lag']) if len(fossil_first_sig) > 0 else None

    print(f"\n  First significant lag (p<0.10):")
    print(f"    Water: {w_first}y" if w_first else "    Water: never significant")
    print(f"    Fossil: {f_first}y" if f_first else "    Fossil: never significant")

    if w_first and f_first and w_first < f_first:
        print(f"\n  -> PASS: Water leads fossil by {f_first - w_first} years")
    elif w_first and not f_first:
        print(f"\n  -> PASS: Water significant, fossil never significant")
    elif w_first and f_first:
        print(f"\n  -> FAIL: Fossil leads or ties water")
    else:
        print(f"\n  -> INCONCLUSIVE: Neither significantly predicts GDP growth")

    return df_cc, water_peak, fossil_peak


# ─────────────────────────────────────────────────────────────────────────────
# STRATEGY 3: Granger Causality — Water-era specificity
# ─────────────────────────────────────────────────────────────────────────────

def strategy_3_granger_mechanism(df_gdp, df_ngram):
    """Granger causality for water and fossil separately, by sub-period.

    The thesis predicts:
    - 1700-1810: Water Granger-causes GDP, Fossil does NOT
    - 1810-1900: Fossil Granger-causes GDP, Water does NOT

    This is the TIMING test. Not who has bigger effect, but who comes FIRST.
    """
    print("\n" + "=" * 70)
    print("STRATEGY 3: GRANGER CAUSALITY BY SUB-PERIOD")
    print("Who Granger-causes GDP in which era?")
    print("=" * 70)

    from statsmodels.tsa.stattools import grangercausalitytests

    results = {}
    for period, yr_start, yr_end in [
        ('Water Era (1700-1810)', 1700, 1810),
        ('Fossil Era (1810-1900)', 1810, 1900),
    ]:
        gdp_sub = df_gdp.loc[yr_start:yr_end, 'GBR']
        ngram_sub = df_ngram.loc[yr_start:yr_end]

        water = vocab_intensity(ngram_sub, WATER_INFRA)
        fossil = vocab_intensity(ngram_sub, FOSSIL_TERMS)

        print(f"\n  {period}:")

        for label, vocab_series in [('Water Infra', water), ('Fossil/Steam', fossil)]:
            # First-difference for stationarity
            dg = gdp_sub.diff().dropna()
            dv = vocab_series.diff().dropna()
            common = dg.index.intersection(dv.index)
            if len(common) < 20:
                print(f"    {label} -> GDP: insufficient data (N={len(common)})")
                results[f'{period}_{label}'] = {'p': np.nan}
                continue

            data = pd.DataFrame({'GDP': dg.loc[common], 'Vocab': dv.loc[common]}).dropna()

            try:
                gc = grangercausalitytests(data[['GDP', 'Vocab']], maxlag=5, verbose=False)
                # Best lag by AIC-like criterion (lowest p-value)
                best_lag = min(gc.keys(), key=lambda k: gc[k][0]['ssr_ftest'][1])
                f_stat = gc[best_lag][0]['ssr_ftest'][0]
                p_val = gc[best_lag][0]['ssr_ftest'][1]
                sig = '***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'ns'
                print(f"    {label} -> GDP: F={f_stat:.2f}, p={p_val:.4f} {sig} (lag={best_lag})")
                results[f'{period}_{label}'] = {'p': p_val, 'f': f_stat, 'lag': best_lag}
            except Exception as e:
                print(f"    {label} -> GDP: error ({e})")
                results[f'{period}_{label}'] = {'p': np.nan}

    # Verdict
    w_pre = results.get('Water Era (1700-1810)_Water Infra', {}).get('p', np.nan)
    f_pre = results.get('Water Era (1700-1810)_Fossil/Steam', {}).get('p', np.nan)
    w_post = results.get('Fossil Era (1810-1900)_Water Infra', {}).get('p', np.nan)
    f_post = results.get('Fossil Era (1810-1900)_Fossil/Steam', {}).get('p', np.nan)

    print(f"\n  TIMING VERDICT:")
    water_first = (not np.isnan(w_pre)) and w_pre < 0.10
    fossil_not_first = np.isnan(f_pre) or f_pre > 0.10
    fossil_later = (not np.isnan(f_post)) and f_post < 0.10

    if water_first and fossil_not_first:
        print("  -> STRONG: Water Granger-causes GDP in water-era, fossil does NOT")
        print("     This confirms water as temporal first-mover")
    elif water_first:
        print("  -> MODERATE: Water Granger-causes GDP in water-era (but fossil does too)")
    else:
        print("  -> WEAK: Cannot confirm water temporal precedence via Granger")

    if fossil_later:
        print("  -> Fossil takes over in steam-era (Tvedt narrative supported)")

    return results


# ─────────────────────────────────────────────────────────────────────────────
# STRATEGY 4: DiD with Vocabulary-Derived Divergence Onset
# ─────────────────────────────────────────────────────────────────────────────

def strategy_4_divergence_onset(df_gdp, df_ngram):
    """Test whether water vocabulary predicts the ONSET of divergence.

    Compute when GBR GDP first sustainably exceeds the European average.
    Then test: did water vocabulary growth precede this onset?
    """
    print("\n" + "=" * 70)
    print("STRATEGY 4: VOCABULARY-PREDICTED DIVERGENCE ONSET")
    print("Did water growth precede the GDP breakaway?")
    print("=" * 70)

    # Find divergence onset: when GBR GDP exceeds EUR average by >20%
    eur_avg = df_gdp[['NLD', 'FRA']].mean(axis=1)
    ratio = df_gdp['GBR'] / eur_avg
    # Sustained divergence: 10-year rolling mean > 1.10
    ratio_smooth = ratio.rolling(10, center=True, min_periods=5).mean()
    divergence_years = ratio_smooth[ratio_smooth > 1.10].index
    divergence_onset = int(divergence_years[0]) if len(divergence_years) > 0 else None

    print(f"  GDP divergence onset (GBR/EUR > 1.10 sustained): {divergence_onset}")

    # Find vocabulary acceleration onset
    water = vocab_intensity(df_ngram, WATER_INFRA)
    fossil = vocab_intensity(df_ngram, FOSSIL_TERMS)

    # Acceleration = second derivative > 0 sustained
    w_growth = water.diff().rolling(10, center=True, min_periods=5).mean()
    f_growth = fossil.diff().rolling(10, center=True, min_periods=5).mean()

    # Find first sustained positive acceleration
    w_accel_years = w_growth[w_growth > w_growth.quantile(0.75)].index
    f_accel_years = f_growth[f_growth > f_growth.quantile(0.75)].index

    w_onset = int(w_accel_years[0]) if len(w_accel_years) > 0 else None
    f_onset = int(f_accel_years[0]) if len(f_accel_years) > 0 else None

    print(f"  Water vocab acceleration onset: {w_onset}")
    print(f"  Fossil vocab acceleration onset: {f_onset}")

    if divergence_onset and w_onset and f_onset:
        w_lead = divergence_onset - w_onset
        f_lead = divergence_onset - f_onset
        print(f"\n  Water leads GDP divergence by: {w_lead} years")
        print(f"  Fossil leads GDP divergence by: {f_lead} years")

        if w_lead > f_lead and w_lead > 0:
            print(f"  -> PASS: Water vocabulary accelerated {w_lead - f_lead} years BEFORE fossil")
            print(f"     Water anticipated GDP divergence by {w_lead} years")
        elif w_lead > 0:
            print(f"  -> PARTIAL: Water leads GDP but not more than fossil")
        else:
            print(f"  -> FAIL: Water does not lead GDP divergence")
    else:
        print("  -> INCONCLUSIVE: Could not determine onset dates")

    return {
        'divergence_onset': divergence_onset,
        'water_onset': w_onset, 'fossil_onset': f_onset,
        'water_lead': divergence_onset - w_onset if divergence_onset and w_onset else None,
        'fossil_lead': divergence_onset - f_onset if divergence_onset and f_onset else None,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Visualization
# ─────────────────────────────────────────────────────────────────────────────

def plot_mechanism_summary(df_gdp, df_ngram, cc_df, granger_results, onset_results):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # ── Panel A: Cross-Correlation Lag Structure ─────────────────────────
    ax = axes[0, 0]
    ax.plot(cc_df['lag'], cc_df['water_r'], 'o-', color='#1a5276', linewidth=2,
            markersize=5, label='Water Infra')
    ax.plot(cc_df['lag'], cc_df['fossil_r'], 's-', color='#e74c3c', linewidth=2,
            markersize=5, label='Fossil/Steam')
    ax.axhline(y=0, color='black', linewidth=0.8)
    # Significance threshold (approximate)
    n = 200 - cc_df['lag'].max()
    sig_thresh = 1.96 / np.sqrt(n)
    ax.axhline(y=sig_thresh, color='gray', linewidth=1, linestyle=':', alpha=0.5)
    ax.axhline(y=-sig_thresh, color='gray', linewidth=1, linestyle=':', alpha=0.5)
    ax.set_xlabel('Lag (years)', fontsize=11)
    ax.set_ylabel('Cross-correlation with GDP growth', fontsize=11)
    ax.set_title('A — Cross-Correlation: Who Leads GDP?', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.2)

    # ── Panel B: Granger Causality by Sub-Period ─────────────────────────
    ax = axes[0, 1]
    categories = ['Water\n1700-1810', 'Fossil\n1700-1810',
                   'Water\n1810-1900', 'Fossil\n1810-1900']
    keys = ['Water Era (1700-1810)_Water Infra', 'Water Era (1700-1810)_Fossil/Steam',
            'Fossil Era (1810-1900)_Water Infra', 'Fossil Era (1810-1900)_Fossil/Steam']
    pvals = [granger_results.get(k, {}).get('p', 1.0) for k in keys]
    colors = ['#1a5276', '#e74c3c', '#1a5276', '#e74c3c']
    # Plot -log10(p) so significant results are taller
    log_p = [-np.log10(max(p, 1e-10)) for p in pvals]
    for idx, (lp, c, a) in enumerate(zip(log_p, colors, [1.0, 1.0, 0.5, 0.5])):
        ax.bar(idx, lp, color=c, edgecolor='black', linewidth=0.5, width=0.6, alpha=a)
    ax.axhline(y=-np.log10(0.05), color='orange', linewidth=2, linestyle='--',
               label='p = 0.05 threshold')
    ax.axhline(y=-np.log10(0.10), color='gray', linewidth=1, linestyle=':',
               label='p = 0.10 threshold')
    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_ylabel('-log10(p-value)', fontsize=11)
    ax.set_title('B — Granger Causality by Era', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.2, axis='y')

    # ── Panel C: Vocabulary Trajectories + GDP ───────────────────────────
    ax = axes[1, 0]
    water = normalize(vocab_intensity(df_ngram, WATER_INFRA))
    fossil = normalize(vocab_intensity(df_ngram, FOSSIL_TERMS))

    ax2 = ax.twinx()
    ax.plot(df_gdp.index, df_gdp['GBR'], color='gray', linewidth=2.5,
            alpha=0.7, label='GBR GDP/cap')
    ax.plot(df_gdp.index, df_gdp[['NLD', 'FRA']].mean(axis=1), color='gray',
            linewidth=1.5, linestyle='--', alpha=0.5, label='EUR avg GDP/cap')
    ax2.plot(water.index, water, color='#1a5276', linewidth=2,
             label='Water Intensity')
    ax2.plot(fossil.index, fossil, color='#e74c3c', linewidth=2,
             label='Fossil Intensity')

    if onset_results.get('water_onset'):
        ax.axvline(x=onset_results['water_onset'], color='#1a5276',
                   linewidth=1.5, linestyle=':', alpha=0.7)
    if onset_results.get('fossil_onset'):
        ax.axvline(x=onset_results['fossil_onset'], color='#e74c3c',
                   linewidth=1.5, linestyle=':', alpha=0.7)
    if onset_results.get('divergence_onset'):
        ax.axvline(x=onset_results['divergence_onset'], color='green',
                   linewidth=2, linestyle='--', alpha=0.7)
        ax.annotate(f"GDP divergence\n{onset_results['divergence_onset']}",
                    xy=(onset_results['divergence_onset'], df_gdp['GBR'].max() * 0.5),
                    fontsize=9, color='green', fontweight='bold')

    ax.set_xlabel('Year', fontsize=11)
    ax.set_ylabel('GDP per capita', fontsize=11)
    ax2.set_ylabel('Normalized Vocab Intensity', fontsize=11)
    ax.set_title('C — Temporal Sequence: Water -> GDP -> Fossil', fontsize=13, fontweight='bold')
    ax.legend(loc='upper left', fontsize=8)
    ax2.legend(loc='center left', fontsize=8)
    ax.grid(True, alpha=0.2)

    # ── Panel D: Onset Timeline ──────────────────────────────────────────
    ax = axes[1, 1]
    events = []
    if onset_results.get('water_onset'):
        events.append(('Water Vocab\nAcceleration', onset_results['water_onset'], '#1a5276'))
    if onset_results.get('fossil_onset'):
        events.append(('Fossil Vocab\nAcceleration', onset_results['fossil_onset'], '#e74c3c'))
    if onset_results.get('divergence_onset'):
        events.append(('GDP\nDivergence', onset_results['divergence_onset'], '#27ae60'))

    events.sort(key=lambda x: x[1])
    for i, (label, year, color) in enumerate(events):
        ax.barh(i, year - 1690, left=1690, color=color, height=0.5,
                edgecolor='black', linewidth=0.5)
        ax.text(year + 2, i, f'{year}', va='center', fontsize=12, fontweight='bold')
        ax.text(1692, i, label, va='center', fontsize=11, color=color, fontweight='bold')

    ax.set_xlim(1690, 1850)
    ax.set_xlabel('Year', fontsize=11)
    ax.set_yticks([])
    ax.set_title('D — Onset Timeline: Who Came First?', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.2, axis='x')

    w_lead = onset_results.get('water_lead')
    f_lead = onset_results.get('fossil_lead')
    if w_lead and f_lead:
        ax.text(0.5, -0.15,
                f'Water leads GDP by {w_lead}y | Fossil leads GDP by {f_lead}y | '
                f'Water leads Fossil by {w_lead - f_lead}y',
                transform=ax.transAxes, ha='center', fontsize=11,
                fontweight='bold', style='italic')

    fig.suptitle('Iteration 07: Water as First Mover — Timing Evidence',
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(DATA_DIR / 'did_water_mechanism_iter07.png', dpi=150, bbox_inches='tight')
    print(f"\n  Saved: data/did_water_mechanism_iter07.png")
    plt.close()


# ─────────────────────────────────────────────────────────────────────────────
# Master runner
# ─────────────────────────────────────────────────────────────────────────────

def run_water_mechanism():
    print("=" * 70)
    print("ITERATION 07: WATER AS FIRST MOVER — TIMING EVIDENCE")
    print("The thesis is about TIMING, not magnitude")
    print("=" * 70)

    df_gdp, df_ngram = load_data()

    seq_results = strategy_1_sequential_periods(df_gdp, df_ngram)
    cc_df, w_peak, f_peak = strategy_2_cross_correlation(df_gdp, df_ngram)
    granger_results = strategy_3_granger_mechanism(df_gdp, df_ngram)
    onset_results = strategy_4_divergence_onset(df_gdp, df_ngram)

    plot_mechanism_summary(df_gdp, df_ngram, cc_df, granger_results, onset_results)

    # ── Final Scorecard ──────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("ITERATION 07: FIRST-MOVER TIMING SCORECARD")
    print("=" * 70)

    # Test 1: Sequential periods
    w_pre_p = seq_results.get('Water Era (1700-1810)', {}).get('water_p', 1)
    f_pre_p = seq_results.get('Water Era (1700-1810)', {}).get('fossil_p', 1)

    # Test 2: Cross-correlation
    w_first_sig = cc_df[cc_df['water_p'] < 0.10]
    f_first_sig = cc_df[cc_df['fossil_p'] < 0.10]
    w_first = int(w_first_sig.iloc[0]['lag']) if len(w_first_sig) > 0 else 999
    f_first = int(f_first_sig.iloc[0]['lag']) if len(f_first_sig) > 0 else 999

    # Test 3: Granger by era
    gc_w_pre = granger_results.get('Water Era (1700-1810)_Water Infra', {}).get('p', 1)
    gc_f_pre = granger_results.get('Water Era (1700-1810)_Fossil/Steam', {}).get('p', 1)

    # Test 4: Onset timing
    w_lead = onset_results.get('water_lead') or 0
    f_lead = onset_results.get('fossil_lead') or 0

    tests = [
        ("Water predicts GDP in water-era", w_pre_p < 0.10,
         f"p={w_pre_p:.4f}"),
        ("Fossil does NOT predict GDP in water-era", f_pre_p > 0.10,
         f"p={f_pre_p:.4f}"),
        ("Water cross-corr leads fossil", w_first < f_first,
         f"water first sig at lag={w_first}, fossil at lag={f_first}"),
        ("Granger: water-era water->GDP", gc_w_pre < 0.10,
         f"p={gc_w_pre:.4f}"),
        ("Granger: water-era fossil NOT->GDP", gc_f_pre > 0.10,
         f"p={gc_f_pre:.4f}"),
        ("Water vocab onset precedes fossil", w_lead > f_lead,
         f"water leads GDP by {w_lead}y, fossil by {f_lead}y"),
    ]

    for name, passed, detail in tests:
        icon = "+" if passed else "-"
        status = "PASS" if passed else "FAIL"
        print(f"  [{icon}] {name:<45} {status:<6} ({detail})")

    n_pass = sum(1 for _, p, _ in tests if p)
    print(f"\n  Overall: {n_pass}/{len(tests)} timing tests passed")

    if n_pass >= 4:
        print("  CONCLUSION: STRONG evidence for water as temporal first-mover")
    elif n_pass >= 2:
        print("  CONCLUSION: MODERATE evidence for water as temporal first-mover")
    else:
        print("  CONCLUSION: WEAK evidence — timing advantage not clearly demonstrated")

    print("=" * 70)

    return {
        'sequential': seq_results,
        'cross_corr': cc_df,
        'granger': granger_results,
        'onset': onset_results,
        'n_pass': n_pass, 'n_tests': len(tests)
    }


if __name__ == '__main__':
    run_water_mechanism()
