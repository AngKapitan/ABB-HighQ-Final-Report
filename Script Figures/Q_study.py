import numpy as np
import matplotlib.pyplot as plt
import math

# Set the global font family to Arial
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

# Force math mode text to also use Arial
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Arial'
plt.rcParams['mathtext.it'] = 'Arial:italic'
plt.rcParams['mathtext.bf'] = 'Arial:bold'

# ---------------------------------------------------------
# 1. User-Defined Specifications
# ---------------------------------------------------------
P_out = 100000.0       # Max power: 100 kW
V_in_min = 600.0       # Minimum input voltage
V_in_nom = 1000.0      # Nominal input voltage
V_out_max = 1000.0     # Maximum output voltage
V_out_nom = 1000.0     # Nominal output voltage
n = 1.0                # Transformer ratio

L_r = 20.1e-6          # Resonant inductor (H)
C_r = 1.4e-6           # Resonant capacitor (F)

# ---------------------------------------------------------
# 2. Derived Parameters
# ---------------------------------------------------------
Mg_max = (n * V_out_max) / V_in_min
Mg_nom = (n * V_out_nom) / V_in_nom

f_r = 1 / (2 * math.pi * math.sqrt(L_r * C_r))
Z_r = math.sqrt(L_r / C_r)

R_o = (1000.0**2) / P_out 
R_ac = (8 / (math.pi**2)) * R_o
Q_max = Z_r / R_ac

# ---------------------------------------------------------
# 3. Sweep k to find a valid design
# ---------------------------------------------------------
f_n_values = np.linspace(0.2, 1.5, 1000) 
k_test_values = [3, 4, 5, 6, 7, 10] 

fig, ax = plt.subplots(figsize=(8, 6))

for k in k_test_values:
    term1 = Q_max * f_n_values * (1 / k + 2)
    term2 = (Q_max / f_n_values) * (2 / k + 2)
    term3 = Q_max / (k * f_n_values**3)
    
    gain_curve = 1 / np.sqrt((term1 - term2 + term3)**2 + (1 / k - 1 / (k * f_n_values**2) + 1)**2)
    
    ax.plot(f_n_values, gain_curve, linewidth=1.5, label=f'k = {k}')

# Plot boundary conditions
ax.axhline(Mg_nom, color='black', linestyle='--', linewidth=2, label=f'Nominal Gain ({Mg_nom:.1f})')

# Mark nominal operating point
ax.plot(1.0, Mg_nom, 'ko', markersize=8)

ax.set_title(f'Gain Curve at Full Load $Q = {Q_max:.2f}$', fontsize=20)
ax.set_xlabel('Normalized Frequency ($f_n$)', fontsize=16)
ax.set_ylabel('Voltage Gain ($M_g$)', fontsize=16)
ax.set_ylim(0.5, 1.8)
ax.set_xlim(0.2, 1.5)
ax.grid(True, linestyle=':', alpha=0.7)
ax.legend(loc='upper right')

plt.tight_layout()

# Save as PDF before showing
fig.savefig('k_sweep_full_load.pdf', format='pdf', bbox_inches='tight')
plt.show()