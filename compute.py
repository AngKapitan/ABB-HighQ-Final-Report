import math
import numpy as np
from scipy import integrate

# ==============================================================================
# 1. CONSTANTS & DESIGN PARAMETERS
# ==============================================================================
# Electrical Specs
I_p_rms = 10.0          # A
J_target = 5.0e6        # A/m^2
V_pri_pk = 100.0        # V
f_s = 28.5e3            # Hz
T_s = 1 / f_s           # s
t_dead = 400e-9         # s

# Material Specs
sigma = 5.96e7          # S/m (Copper)
mu_0 = 4 * math.pi * 1e-7 # H/m
k_igse = 0.0620
alpha = 1.7066
beta = 2.535

# Geometric Specs (m)
w_wire = 0.30e-3
N_p = 8
d_inter = 0.1e-3
d_clear = 1.0e-3
l_core = 50.86e-3       # Core length
w_cent = 10.0e-3        # Center leg width
w_out = 5.0e-3          # Outer leg width
l_g = 0.1e-3            # Gap length

# ==============================================================================
# 2. DIMENSIONING & VOLUME
# ==============================================================================
# Wire height
h_wire = I_p_rms / (J_target * w_wire)

# Window dimensions
l_win = h_wire + 2 * d_clear
w_win = 2 * N_p * w_wire + (2 * N_p - 1) * d_inter + 2 * d_clear

# Core outer dimensions
w_core = w_cent + 2 * w_win + 2 * w_out
h_core = l_win + 2 * w_out

# Transformer bounding box
l_trans = l_core + 2 * w_win
w_trans = w_core
h_trans = h_core
V_box = l_trans * w_trans * h_trans

# Magnetic core volume
V_core = l_core * ((w_core * h_core) - (2 * (w_win * l_win) + l_g * (2 * w_out + w_cent)))

# ==============================================================================
# 3. WINDING GEOMETRY & COPPER LOSS
# ==============================================================================
# Mean turn lengths
lt_1 = 2 * ((w_cent + w_wire + 2 * d_clear) + (l_core + w_wire + 2 * d_clear))
d = 8 * (w_wire + d_inter)
S_total = N_p * (2 * lt_1 + (2 * N_p - 1) * d)

# DC Resistance
R_dc = S_total / (sigma * h_wire * w_wire)

# AC Resistance (Dowell)
delta = 1 / math.sqrt(math.pi * f_s * mu_0 * sigma)
xi = w_wire / delta

m = 1 # Fully interleaved
term1 = (math.sinh(xi) + math.sin(xi)) / (math.cosh(xi) - math.cos(xi))
term2 = (2 * m**2 - 1) * (math.sinh(xi) - math.sin(xi)) / (math.cosh(xi) + math.cos(xi))
F_ac = (xi / 2) * (term1 + term2)

R_ac = F_ac * R_dc
P_wind = (I_p_rms**2) * R_ac

# ==============================================================================
# 4. CORE LOSS (iGSE)
# ==============================================================================
A_calc = l_core * w_cent
Delta_B = (V_pri_pk * (T_s / 2)) / (N_p * A_calc)

t_active = (T_s / 2) - t_dead
dB_dt = Delta_B / t_active

# Waveform coefficient k_i
def ki_integrand(theta):
    return (abs(math.cos(theta))**alpha) * (2**(beta - alpha))

ki_integral, _ = integrate.quad(ki_integrand, 0, 2 * math.pi)
k_i = k_igse / (2 * (math.pi**(alpha - 1)) * ki_integral)

# Volumetric core loss integral
def core_loss_integrand(t):
    return k_i * (dB_dt**alpha) * (Delta_B**(beta - alpha))

# Integrate over the switching period (assuming symmetric excitation)
E_cycle, _ = integrate.quad(core_loss_integrand, 0, T_s)
P_core = (E_cycle / T_s) * V_core

P_total = P_wind + P_core

# ==============================================================================
# 5. OUTPUT GENERATOR
# ==============================================================================
print("-" * 50)
print(" APPENDIX A: VERIFICATION SCRIPT OUTPUT")
print("-" * 50)
print(f"h_wire:        {h_wire*1000:.2f} mm")
print(f"l_win:         {l_win*1000:.2f} mm")
print(f"w_win:         {w_win*1000:.2f} mm")
print(f"w_core:        {w_core*1000:.2f} mm")
print(f"h_core:        {h_core*1000:.2f} mm")
print(f"l_trans:       {l_trans*1000:.2f} mm")
print(f"V_box:         {V_box*1e6:.1f} mm^3 ({V_box*1e6/1000:.1f} cm^3)")
print(f"V_core:        {V_core*1e6:.0f} mm^3 ({V_core*1e6/1000:.2f} cm^3)")
print("-" * 50)
print(f"lt_1:          {lt_1*1000:.2f} mm")
print(f"d:             {d*1000:.2f} mm")
print(f"S_total:       {S_total:.3f} m")
print(f"R_dc:          {R_dc*1000:.2f} mOhm")
print(f"delta:         {delta*1000:.3f} mm")
print(f"xi:            {xi:.3f}")
print(f"F_ac:          {F_ac:.3f}")
print(f"R_ac:          {R_ac*1000:.2f} mOhm")
print(f"P_wind:        {P_wind:.2f} W")
print("-" * 50)
print(f"A_calc:        {A_calc*1e6:.1f} mm^2")
print(f"Delta B:       {Delta_B:.3f} T")
print(f"dB/dt:         {dB_dt:.0f} T/s")
print(f"k_i:           {k_i:.3e}")
print(f"P_core:        {P_core:.2f} W")
print("-" * 50)
print(f"TOTAL LOSS:    {P_total:.2f} W")
print("-" * 50)