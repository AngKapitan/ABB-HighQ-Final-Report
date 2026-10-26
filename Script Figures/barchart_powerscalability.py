import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np

# --- SET GLOBAL FONT TO ARIAL ---
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial']
})

# --- DATA INPUT ---
labels = [
    '1 kW \n(TrE-1/TrF-1)', 
    '10 kW \n(TrE-10/TrF-10)', 
    '100 kW \n(TrE-100/TrF-100)'
]

edge_forced = np.array([36.8, 78.2, 210.6])
flat_forced = np.array([21.2, 24.2, 37.0])

# --- COMMON PLOTTING SETUP ---
plt.style.use('seaborn-v0_8-whitegrid')
width = 0.35
x = np.arange(len(labels))

# Bar Colors
color_flat = '#084594'  # Deep Blue for Flatwise
color_edge = '#4292c6'  # Medium Blue for Edgewise

# High-Contrast Trendline Colors
line_flat =  '#084594'   # Crimson Red (contrasts with blue & highlights heat rise)
line_edge = '#4292c6'  # Near-Black (contrasts sharply with both blues)

# Shadow Effect Constants
shift_x = 0.04
shadow_color = '#777777'
shadow_alpha = 0.3

# ==============================================================================
# SCENARIO 2: FORCED-AIR COOLING
# ==============================================================================
fig2, ax2 = plt.subplots(figsize=(8, 8))

# 1. Shadows
ax2.bar(x - width/2 + shift_x, edge_forced, width, color=shadow_color, alpha=shadow_alpha, zorder=1)
ax2.bar(x + width/2 + shift_x, flat_forced, width, color=shadow_color, alpha=shadow_alpha, zorder=1)

# 2. Main Bars
ax2.bar(x - width/2, edge_forced, width, label='Edgewise-wound (Conv.)', color=color_edge, edgecolor='black', linewidth=0.7, zorder=3)
ax2.bar(x + width/2, flat_forced, width, label='Flatwise-wound (Proposed)', color=color_flat, edgecolor='black', linewidth=0.7, zorder=3)

# 3. High-Contrast Lines Connecting the Peaks (with white halo so they don't blend into bars)
line_halo = [pe.Stroke(linewidth=5, foreground='white'), pe.Normal()]

ax2.plot(x - width/2, edge_forced, color=line_edge, linestyle='--', linewidth=2.5,
         marker='o', markersize=8, markerfacecolor='white', markeredgecolor=line_edge, 
         markeredgewidth=2, path_effects=line_halo, zorder=4)

ax2.plot(x + width/2, flat_forced, color=line_flat, linestyle='--', linewidth=2.5,
         marker='s', markersize=7, markerfacecolor='white', markeredgecolor=line_flat, 
         markeredgewidth=2, path_effects=line_halo, zorder=4)

# 4. Annotations (with white text halo and nudge on 78.2°C to avoid line overlap)
text_halo = [pe.Stroke(linewidth=3.5, foreground='white'), pe.Normal()]

for i in range(len(x)):
    # Nudge the middle (10 kW) Edgewise label slightly left so the steep line misses it
    edge_x_pos = (x[i] - width/2 - 0.06) if i == 1 else (x[i] - width/2)
    
    # Edgewise Text
    ax2.text(edge_x_pos, edge_forced[i] + 4.5, f'{edge_forced[i]:.1f}°C', 
             ha='center', va='bottom', fontsize=14, fontweight='bold', 
             color='#222222', path_effects=text_halo, zorder=5)
    
    # Flatwise Text
    ax2.text(x[i] + width/2, flat_forced[i] + 4.5, f'{flat_forced[i]:.1f}°C', 
             ha='center', va='bottom', fontsize=14, fontweight='bold', 
             color='#222222', path_effects=text_halo, zorder=5)

# 5. Formatting
ax2.set_ylabel('Peak Temperature (°C)', fontsize=18, fontweight='bold')
ax2.set_xlabel('Transformer Operating Power', fontsize=16, fontweight='bold', labelpad=10)
ax2.set_xticks(x)
ax2.set_xticklabels(labels, fontsize=20)
ax2.set_ylim(0, 225)
ax2.tick_params(axis='y', labelsize=20)
ax2.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)

# Legend
ax2.legend(loc='upper left', fontsize=18, frameon=True, framealpha=1, shadow=True, fancybox=True)

plt.tight_layout()
plt.savefig('thermal_forced_grouped_scale.pdf', format='pdf', bbox_inches='tight')
plt.savefig('thermal_forced_grouped_scale.svg', format='svg', bbox_inches='tight')
plt.show()