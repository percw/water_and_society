import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path
import sys

# Setup paths to import from src
PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_DIR / "src"))

from did_analysis import (
    fetch_real_maddison, 
    derive_treatment_year, 
    run_event_study, 
    run_placebo_vocabulary_tournament,
    DATA_DIR, CH_TRANSPORT, CH_POWER, PLACEBO_STEAM_MECH
)

# ── JEH formatting ──────────────────────────────────────────────────────────
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif']
mpl.rcParams['figure.dpi'] = 300
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['axes.edgecolor'] = 'black'
mpl.rcParams['axes.linewidth'] = 1.0


def plot_figure_one_jeh(df_gdp, t0):
    ngram_path = DATA_DIR / 'ngram_english.csv'
    if not ngram_path.exists():
        return

    df_ngram = pd.read_csv(ngram_path, index_col='Year')

    transport_terms = [w for w in CH_TRANSPORT if w in df_ngram.columns]
    fossil_terms = [w for w in PLACEBO_STEAM_MECH if w in df_ngram.columns]

    transport_raw = df_ngram[transport_terms].sum(axis=1).rolling(5).mean()
    fossil_raw = df_ngram[fossil_terms].sum(axis=1).rolling(5).mean()

    ctrl = df_gdp[['NLD', 'FRA']].mean(axis=1)
    gdp_gap = df_gdp['GBR'] - ctrl

    def norm01(s):
        s = s.dropna()
        return (s - s.min()) / (s.max() - s.min() + 1e-20)

    t_norm = norm01(transport_raw)
    f_norm = norm01(fossil_raw)
    g_norm = norm01(gdp_gap)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.fill_between(g_norm.index, 0, g_norm.values, alpha=0.08, color='black')
    ax.plot(g_norm.index, g_norm.values, color='black', linewidth=1.5,
            linestyle='-', label='GDP Gap (GBR − Controls)')

    ax.plot(t_norm.index, t_norm.values, color='dimgray', linewidth=2.5,
            linestyle='--', label='Hydro-Infrastructure Lexicon')

    ax.plot(f_norm.index, f_norm.values, color='silver', linewidth=2.0,
            linestyle=':', label='Fossil/Steam Lexicon')

    ax.axvline(x=t0, color='black', linewidth=1.2, linestyle='-.', zorder=0)

    # Cleaned ticks and minimalist axes
    ax.tick_params(direction='in', length=5, width=1)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Normalized Index', fontsize=12)
    
    # Internal, unboxed legend
    ax.legend(fontsize=11, loc='upper left', frameon=False)
    ax.set_xlim(1700, 1900)
    ax.set_ylim(-0.05, 1.05)
    
    # Minimalist Academic standard: no top/right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(DATA_DIR / 'did_figure_one.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_event_study_jeh(df_es, t0):
    fig, ax = plt.subplots(figsize=(8, 5))

    bins = df_es['bin'].values
    coefs = df_es['coef'].values
    ci_lo = df_es['ci_low'].values
    ci_hi = df_es['ci_high'].values

    ax.fill_between(bins, ci_lo, ci_hi, alpha=0.15, color='dimgray', linewidth=0)
    ax.plot(bins, coefs, 'o-', color='black', linewidth=1.5, markersize=4, zorder=5)
    
    # Zero line
    ax.axhline(y=0, color='black', linewidth=0.8, linestyle='-', zorder=1)
    
    # T0 Line
    ax.axvline(x=0, color='dimgray', linewidth=1.2, linestyle='--', zorder=1)

    ax.tick_params(direction='in')
    ax.set_xlabel('Years Relative to Structural Break ($T_0=1766$)', fontsize=11)
    ax.set_ylabel('Treatment Effect (GDP per capita)', fontsize=11)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(DATA_DIR / 'did_event_study.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_vocabulary_tournament_jeh(tournament):
    if not tournament:
        return

    n = len(tournament)
    cols = min(n, 3)
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 3.5 * rows), sharey=True)
    if n == 1:
        axes = np.array([axes])
    axes = axes.flatten()

    panel_labels = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)', '(g)', '(h)']

    for i, (cat_name, res) in enumerate(tournament.items()):
        ax = axes[i]
        df_es = res['event_study']
        bins = df_es['bin'].values
        coefs = df_es['coef'].values
        ci_lo = df_es['ci_low'].values
        ci_hi = df_es['ci_high'].values

        # Strict monochrome distinction without spelling it out
        color = 'black' if res['clean'] else 'silver'
        line_style = '-' if res['clean'] else '--'
        alpha_val = 0.15 if res['clean'] else 0.08
        lw = 1.5 if res['clean'] else 1.0

        ax.fill_between(bins, ci_lo, ci_hi, alpha=alpha_val, color=color, lw=0)
        ax.plot(bins, coefs, marker='o', linestyle=line_style, color=color, linewidth=lw, markersize=3)
        ax.axhline(y=0, color='black', linewidth=0.6)
        ax.axvline(x=0, color='dimgray', linewidth=1.0, linestyle=':')

        # Clean, strictly academic titles
        clean_cat = cat_name.replace(chr(10), " ").split(' (')[0]
        ax.set_title(f'{panel_labels[i]} {clean_cat}', fontsize=10, loc='left')
        
        ax.tick_params(direction='in', labelsize=9)
        if i >= len(tournament) - cols:
            ax.set_xlabel('Years from Break', fontsize=10)
        
        if i % cols == 0:
            ax.set_ylabel('Treatment Effect', fontsize=10)
            
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    plt.tight_layout()
    plt.savefig(DATA_DIR / 'did_vocab_tournament.png', dpi=300, bbox_inches='tight')
    plt.close()


def main():
    print("Generating Academic/JEH Format Plots (Iterated Minimalist Edition)...")
    df_gdp = fetch_real_maddison(force=False)
    
    ngram_path = DATA_DIR / 'ngram_english.csv'
    if ngram_path.exists():
        df_ngram = pd.read_csv(ngram_path, index_col='Year')
        t0, _ = derive_treatment_year(df_ngram)
    else:
        t0 = 1766
        
    print(f"Using T0 = {t0}")
    
    plot_figure_one_jeh(df_gdp, t0)
    print("  ✓ Saved JEH format: data/did_figure_one.png")
    
    df_es, _ = run_event_study(df_gdp, t0, bin_width=5)
    plot_event_study_jeh(df_es, t0)
    print("  ✓ Saved JEH format: data/did_event_study.png")
    
    tournament = run_placebo_vocabulary_tournament(df_gdp, t0)
    plot_vocabulary_tournament_jeh(tournament)
    print("  ✓ Saved JEH format: data/did_vocab_tournament.png")
    
    print("All final JEH format plots successfully generated.")

if __name__ == '__main__':
    main()
