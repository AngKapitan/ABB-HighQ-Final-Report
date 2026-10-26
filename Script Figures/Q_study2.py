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
# 1. Nominal Operating Specifications
# ---------------------------------------------------------
P_out_max = 100000.0   # 100 kW Full Scale
V_in_nom = 1000.0      # Nominal Input
V_out_nom = 1000.0     # Nominal Output
n = 1.0                # 1:1 Ratio

L_r = 20.1e-6          # Resonant inductor (H)
C_r = 1.4e-6           # Resonant capacitor (F)
fixed_k = 10.0         # Locked-in inductance ratio

# ---------------------------------------------------------
# 2. Derived Parameters
# ---------------------------------------------------------
Mg_nom = (n * V_out_nom) / V_in_nom 

f_r = 1 / (2 * math.pi * math.sqrt(L_r * C_r))
Z_r = math.sqrt(L_r / C_r)

# Calculate Q for different load percentages
load_steps = [0.1, 0.25, 0.5, 0.75, 1.0] 
Q_values = []

for load in load_steps:
    P_current = P_out_max * load
    R_o = (V_out_nom**2) / P_current 
    R_ac = (8 / (math.pi**2)) * R_o
    Q_values.append(Z_r / R_ac)

# ---------------------------------------------------------
# 3. Plotting the Q Sweep
# ---------------------------------------------------------
f_n_values = np.linspace(0.2, 1.5, 1000) 
fig, ax = plt.subplots(figsize=(8, 6))

for i, Q in enumerate(Q_values):
    term1 = Q * f_n_values * (1 / fixed_k + 2)
    term2 = (Q / f_n_values) * (2 / fixed_k + 2)
    term3 = Q / (fixed_k * f_n_values**3)
    
    gain_curve = 1 / np.sqrt((term1 - term2 + term3)**2 + (1 / fixed_k - 1 / (fixed_k * f_n_values**2) + 1)**2)
    
    ax.plot(f_n_values, gain_curve, linewidth=1.5, label=f'{load_steps[i]*100:.0f}% Load (Q={Q:.2f})')

# Plot boundary conditions
ax.axhline(Mg_nom, color='black', linestyle='--', linewidth=2, label='Nominal Gain (1.0)')
ax.axvline(1.0, color='gray', linestyle=':', linewidth=1.5, label='Resonance (fn = 1)')

# Mark nominal operating point
ax.plot(1.0, 1.0, 'ko', markersize=8)

ax.set_title(f'Gain Curve at $k = {fixed_k}$', fontsize=20)
ax.set_xlabel('Normalized Frequency ($f_n$)', fontsize=16)
ax.set_ylabel('Voltage Gain ($M_g$)', fontsize=16)
ax.set_ylim(0.5, 1.8)
ax.set_xlim(0.2, 1.5)
ax.grid(True, linestyle=':', alpha=0.7)
ax.legend(loc='upper right')

plt.tight_layout()

# Save as PDF before showing
fig.savefig('load_sweep_k10.pdf', format='pdf', bbox_inches='tight')
plt.show()