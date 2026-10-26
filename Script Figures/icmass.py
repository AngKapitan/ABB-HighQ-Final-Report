import matplotlib.pyplot as plt
import numpy as np

# --- DATA INPUT ---
# Categories (Transformer Designators with Thickness)
labels = [
    'Tr1F\n(0.50mm)', 'Tr2F\n(0.30mm)', 'Tr3F\n(0.20mm)', 
    'Tr1E\n(0.20mm)', 'Tr2E\n(0.30mm)', 'Tr3E\n(0.50mm)'
]

# Loss Data (Watts)
winding_loss = np.array([2.5530, 2.3270, 2.2900, 2.3990, 2.2440, 2.1620])
core_loss    = np.array([0.8798, 0.8715, 0.8938, 0.9316, 0.8740, 0.8900])
alum_loss    = np.array([0.1172, 0.0902, 0.0821, 0.0916, 0.0885, 0.0874])

# Total losses for top annotation
total_loss = winding_loss + core_loss + alum_loss

# --- PLOTTING SETUP ---
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))

# Bar config
width = 0.65
x = np.arange(len(labels))

# --- COLOR DEFINITIONS (Shades of Blue) ---
# Darkest for Winding (Top)
color_winding = '#084594'  # Deep Blue
# Medium for Aluminum (Middle)
color_alum    = '#4292c6'  # Medium Blue
# Lightest for Core (Base)
color_core    = '#9ecae1'  # Light Blue

# --- SHADOW EFFECT ---
# Plot gray bars slightly shifted (x+shift, y-shift)
shift_x = 0.06
shift_y = -0.03
shadow_color = '#777777'
shadow_alpha = 0.3

# Shadow 1: Base (Core)
ax.bar(x + shift_x, core_loss, width, color=shadow_color, alpha=shadow_alpha, zorder=1)
# Shadow 2: Middle (Aluminum)
ax.bar(x + shift_x, alum_loss, width, bottom=core_loss, color=shadow_color, alpha=shadow_alpha, zorder=1)
# Shadow 3: Top (Winding)
ax.bar(x + shift_x, winding_loss, width, bottom=core_loss + alum_loss, color=shadow_color, alpha=shadow_alpha, zorder=1)

# --- MAIN STACKED BARS (Winding on Top) ---
# Order: Core (Base) -> Aluminum (Middle) -> Winding (Top)

# 1. Base: Core Loss
ax.bar(x, core_loss, width, label='Core Loss', color=color_core, 
       edgecolor='black', linewidth=0.7, zorder=3)

# 2. Middle: Aluminum Loss
ax.bar(x, alum_loss, width, bottom=core_loss, label='Aluminum Loss', color=color_alum, 
       edgecolor='black', linewidth=0.7, zorder=3)

# 3. Top: Winding Loss
# This is the "on top" bar you requested
ax.bar(x, winding_loss, width, bottom=core_loss + alum_loss, label='Winding Loss', color=color_winding, 
       edgecolor='black', linewidth=0.7, zorder=3)

# --- ANNOTATIONS ---
for i in range(len(x)):
    # A. Total Loss (Above Bar)
    # Increased fontsize from 11 -> 14
    ax.text(x[i], total_loss[i] + 0.08, f'{total_loss[i]:.2f}', 
            ha='center', va='bottom', fontsize=16, fontweight='bold', color='#333333')
    
    # B. Winding Loss Label (Inside the Top Bar)
    # Increased fontsize from 10 -> 13
    # Calculate the vertical center of the winding segment
    y_center_winding = (core_loss[i] + alum_loss[i]) + (winding_loss[i] / 2)
    
    # Plot text in white for contrast against dark blue
    ax.text(x[i], y_center_winding, f'{winding_loss[i]:.2f}', 
            ha='center', va='center', fontsize=15, fontweight='bold', color='white')

# --- FORMATTING ---
# Increased font sizes for labels and title
ax.set_ylabel('Power Loss (W)', fontsize=16, fontweight='bold')
ax.set_xlabel('Transformer Configuration (Thickness)', fontsize=16, fontweight='bold', labelpad=10)

# X-Axis Ticks
ax.set_xticks(x)
# Increased tick label size from 11 -> 14
ax.set_xticklabels(labels, fontsize=16)

# Y-Axis (Add headroom)
ax.set_ylim(0, 4.2)
# Increase Y-axis tick label size
ax.tick_params(axis='y', labelsize=16)

# Legend (Reverse order so Winding is top in legend)
# Increased legend fontsize from 11 -> 14
handles, legend_labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], legend_labels[::-1], loc='upper right', fontsize=10, 
          frameon=True, framealpha=1, shadow=True, fancybox=True)

# Grid
ax.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)

# Group Labels
ylim = ax.get_ylim()[1]
# Increased group label size from 12 -> 15
ax.text(1, ylim*0.92, "Flatwise (F)", ha='center', fontsize=15, fontweight='bold', style='italic', 
        color=color_winding, bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
ax.text(4, ylim*0.92, "Edgewise (E)", ha='center', fontsize=15, fontweight='bold', style='italic', 
        color=color_winding, bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

# --- SHOW PLOT ---
plt.tight_layout()
plt.show()