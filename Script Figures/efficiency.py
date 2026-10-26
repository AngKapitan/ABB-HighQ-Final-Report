import matplotlib.pyplot as plt

# Extracted Data
pin_flat = [52.259, 103.541, 203.74, 300.16, 398.86, 493.26, 587.5, 680.55, 772.85, 862.84, 951.44]
eff_flat = [84.8657, 91.1088, 93.7376, 94.3013, 94.3396, 94.1876, 93.9302, 93.6095, 93.2457, 92.9036, 92.5292]

pin_edge = [51.827, 103.792, 203.93, 300.82, 399.84, 495.22, 589.45, 682.96, 775.16, 865.47, 954.11]
eff_edge = [85.7969, 91.6207, 93.9788, 94.4621, 94.4600, 94.2671, 93.9876, 93.6233, 93.2620, 92.8951, 92.5113]

# Customizable parameters
font_size = 16
line_thickness = 3.0

plt.rcParams.update({'font.size': font_size, 'font.family': 'Arial'})

# Create a plot (10x8 inches)
fig, ax = plt.subplots(figsize=(10, 8))

# Plotting the data - passing linewidth argument
ax.plot(pin_flat, eff_flat, marker='o', linestyle='-', color='blue', linewidth=line_thickness, label='Flatwise-wound')
ax.plot(pin_edge, eff_edge, marker='s', linestyle='-', color='red', linewidth=line_thickness, label='Edgewise-wound')

# Setting axis limits
ax.set_xlim(0, 1000)
ax.set_ylim(80, 100)

# Labels and Title
ax.set_xlabel('Input Power (W)')
ax.set_ylabel('Efficiency (%)')

# Customizable Legend
ax.legend(loc='lower right', frameon=True, fontsize=font_size)

# Grid
ax.grid(True, linestyle=':', alpha=1.0)

# Adjust layout
plt.tight_layout()

# --- EXPORT TO PDF AND SVG ---
plt.savefig("input_power_vs_efficiency.pdf", format="pdf", bbox_inches="tight")
plt.savefig("input_power_vs_efficiency.svg", format="svg", bbox_inches="tight")

plt.show()