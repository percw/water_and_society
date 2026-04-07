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
    DATA_DIR, CH_TRANSPORT
)

# ── JEH formatting ──────────────────────────────────────────────────────────
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif']
mpl.rcParams['figure.dpi'] = 300
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['axes.edgecolor'] = 'black'
mpl.rcParams['axes.linewidth'] = 1.0

def norm01(s):
    s = s.dropna()
    return (s - s.min()) / (s.max() - s.min() + 1e-20)

def main():
    print("Generating Academic/JEH Phase Portrait Segment...")
    df_gdp = fetch_real_maddison(force=False)
    
    ngram_path = DATA_DIR / 'ngram_english.csv'
    if not ngram_path.exists():
        print("Missing ngram data. Cannot generate phase portrait.")
        return
        
    df_ngram = pd.read_csv(ngram_path, index_col='Year')
    
    transport_terms = [w for w in CH_TRANSPORT if w in df_ngram.columns]
    
    # We use a heavier rolling average (e.g., 20 years) to extract the pure structural trajectory
    # without short-term cyclic noise scrambling the phase space orbit.
    transport_raw = df_ngram[transport_terms].sum(axis=1).rolling(20, center=True).mean().dropna()
    
    ctrl = df_gdp[['NLD', 'FRA']].mean(axis=1)
    gdp_gap = (df_gdp['GBR'] - ctrl).rolling(20, center=True).mean().dropna()

    common_years = transport_raw.index.intersection(gdp_gap.index)
    # Clip to the relevant historical transition window
    common_years = common_years[(common_years >= 1700) & (common_years <= 1860)]

    y_val = norm01(transport_raw.loc[common_years])
    x_val = norm01(gdp_gap.loc[common_years])
    
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.suptitle("Figure 4: Phase Space Trajectory of the Hydro-Social Shift", fontsize=15, weight='bold', y=0.96)
    ax.set_title("Mapping the sequence of Semantic Evolution vs. Economic Divergence (1700-1860)", fontsize=11, color='#333333', loc='left', pad=15)
    
    # Plot the structural trajectory line
    ax.plot(x_val, y_val, color='silver', alpha=0.4, linewidth=2.5, zorder=1)
    
    # We use a subtle colormap to imply the passage of time 
    scatter = ax.scatter(x_val, y_val, c=common_years, cmap='viridis_r', s=45, edgecolor='black', linewidth=0.5, zorder=2, alpha=0.8)
    
    # Annotate key decades to guide the eye along the path
    for year in range(1700, 1870, 10):
        if year in common_years:
            # Highlight our critical "turn" decades
            weight = 'bold' if year in [1760, 1770, 1800] else 'normal'
            color = '#2c3e50' if year in [1760, 1770, 1800] else '#555555'
            # offset slightly so text doesn't overlap exactly on the dot
            ax.annotate(str(year), (x_val.loc[year], y_val.loc[year]), 
                        xytext=(7, -2), textcoords='offset points', fontsize=10, 
                        color=color, weight=weight)
            
            # Explicit academic notation for the 1761 shock
            if year == 1760:
                ax.annotate("Bridgewater Shock\n(1761)", (x_val.loc[year], y_val.loc[year]), 
                            xytext=(-80, 45), textcoords='offset points', fontsize=11,
                            arrowprops=dict(arrowstyle="-|>", color='#2c3e50', lw=1.2, shrinkB=5), color='#2c3e50', weight='bold')

    # Draw phase space quadrants locked essentially to the 1760/1761 state
    # This proves visually that Y (Vocabulary) expanded BEFORE X (GDP) expanded.
    ax.axhline(y=y_val.loc[1760], color='#7f8c8d', linestyle=':', linewidth=1.0, alpha=0.6, zorder=0)
    ax.axvline(x=x_val.loc[1760], color='#7f8c8d', linestyle=':', linewidth=1.0, alpha=0.6, zorder=0)
    
    # Neutral fill representing the "Post-Treatment Economic Expansion" quadrant
    ax.fill_betweenx([y_val.loc[1760], 1.1], x_val.loc[1760], 1.1, color='silver', alpha=0.05, zorder=0)
    ax.text(x_val.loc[1760] + 0.02, 1.05, "Post-Shock Trajectory", fontsize=10, color='#7f8c8d', style='italic')

    # Labels
    ax.set_xlabel("Normalized GDP Divergence (Britain − France/Netherlands)", fontsize=12, labelpad=10)
    ax.set_ylabel("Normalized Hydro-Infrastructure Lexicon", fontsize=12, labelpad=10)
    
    # Tufte minimalism
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlim(-0.05, 1.1)
    ax.set_ylim(-0.05, 1.1)
    
    # Save the plot
    output_path = DATA_DIR / 'did_phase_portrait.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"  ✓ Saved Phase Portrait JEH format: {output_path}")

if __name__ == "__main__":
    main()
