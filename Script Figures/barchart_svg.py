import matplotlib.pyplot as plt
import numpy as np

# --- SET GLOBAL FONT TO ARIAL ---
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial']
})

# --- DATA INPUT ---
# X-axis Categories
labels = [
    'Low Profile\n(Tr1E / Tr1F)', 
    'Baseline (Current)\n(Tr2E / Tr2F)', 
    'High Profile\n(Tr3E / Tr3F)'
]

# Peak temperatures (°C) - Grouped by Model [Tr1, Tr2, Tr3]
edge_nat = np.array([61.6, 66.9, 70.9])
flat_nat = np.array([56.1, 56.0, 55.8])

edge_forced = np.array([40.5, 43.6, 47.3])
flat_forced = np.array([30.4, 30.2, 30.2])

# --- COMMON PLOTTING SETUP ---
plt.style.use('seaborn-v0_8-whitegrid')
width = 0.35  # Thinner bars so two can fit per group
x = np.arange(len(labels))

# Color Definitions
color_flat = '#084594'  # Deep Blue for Flatwise
color_edge = '#4292c6'  # Medium Blue for Edgewise

# Shadow Effect Constants
shift_x = 0.04
shift_y = -0.02
shadow_color = '#777777'
shadow_alpha = 0.3

# ==============================================================================
# SCENARIO 1: NATURAL COOLING
# ==============================================================================
fig1, ax1 = plt.subplots(figsize=(8, 8))

# 1. Shadows
ax1.bar(x - width/2 + shift_x, edge_nat, width, color=shadow_color, alpha=shadow_alpha, zorder=1)
ax1.bar(x + width/2 + shift_x, flat_nat, width, color=shadow_color, alpha=shadow_alpha, zorder=1)

# 2. Main Bars
ax1.bar(x - width/2, edge_nat, width, label='Edgewise-wound (Conv.)', color=color_edge, edgecolor='black', linewidth=0.7, zorder=3)
ax1.bar(x + width/2, flat_nat, width, label='Flatwise-wound (Proposed)', color=color_flat, edgecolor='black', linewidth=0.7, zorder=3)

# 3. Annotations
for i in range(len(x)):
    # Edgewise Text
    ax1.text(x[i] - width/2, edge_nat[i] + 1.0, f'{edge_nat[i]:.1f}°C', 
             ha='center', va='bottom', fontsize=14, fontweight='bold', color='#333333')
    # Flatwise Text
    ax1.text(x[i] + width/2, flat_nat[i] + 1.0, f'{flat_nat[i]:.1f}°C', 
             ha='center', va='bottom', fontsize=14, fontweight='bold', color='#333333')

# 4. Formatting
ax1.set_ylabel('Peak Temperature (°C)', fontsize=18, fontweight='bold')
ax1.set_xlabel('Transformer Aspect Ratio Configuration', fontsize=16, fontweight='bold', labelpad=10)
ax1.set_xticks(x)
ax1.set_xticklabels(labels, fontsize=20)
ax1.set_ylim(0, 95) # Headroom for text labels and legend
ax1.tick_params(axis='y', labelsize=20)
ax1.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)

# Legend
ax1.legend(loc='upper right', fontsize=18, frameon=True, framealpha=1, shadow=True, fancybox=True)

plt.tight_layout()
plt.savefig('thermal_natural_grouped.svg', format='svg', bbox_inches='tight')
plt.show()

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

# 3. Annotations
for i in range(len(x)):
    # Edgewise Text
    ax2.text(x[i] - width/2, edge_forced[i] + 0.8, f'{edge_forced[i]:.1f}°C', 
             ha='center', va='bottom', fontsize=14, fontweight='bold', color='#333333')
    # Flatwise Text
    ax2.text(x[i] + width/2, flat_forced[i] + 0.8, f'{flat_forced[i]:.1f}°C', 
             ha='center', va='bottom', fontsize=14, fontweight='bold', color='#333333')

# 4. Formatting
ax2.set_ylabel('Peak Temperature (°C)', fontsize=18, fontweight='bold')
ax2.set_xlabel('Transformer Aspect Ratio Configuration', fontsize=16, fontweight='bold', labelpad=10)
ax2.set_xticks(x)
ax2.set_xticklabels(labels, fontsize=20)
ax2.set_ylim(0, 95) # Synchronized y-axis threshold with Natural Cooling
ax2.tick_params(axis='y', labelsize=20)
ax2.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)

# Legend
ax2.legend(loc='upper right', fontsize=18, frameon=True, framealpha=1, shadow=True, fancybox=True) # Moved to upper right to match

plt.tight_layout()
plt.savefig('thermal_forced_grouped.svg', format='svg', bbox_inches='tight')
plt.show()