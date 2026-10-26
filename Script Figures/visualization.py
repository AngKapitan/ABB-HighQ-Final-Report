import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os
import sys

# Get the directory where this python script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# --- Set Global Plotting Style (Matching your reference script) ---
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Arial']
plt.rcParams.update({'font.size': 14})

# Map the original file prefixes to the new display names and their colors
transformer_map = {
    'E2': {'name': 'Edgewise', 'color': 'red', 'linestyle': '-', 'linewidth': 2, 'alpha': 0.9}, 
    'F2': {'name': 'Flatwise', 'color': 'blue', 'linestyle': '-', 'linewidth': 2, 'alpha': 0.9}
}

# Updated to ONLY load the primary tests
tests = ['meas12open34', 'meas12short34']
data = {}

# ==========================================
# SET YOUR X-AXIS LIMITS HERE (in Hertz)
x_axis_min = 1e2
x_axis_max = 300e3
switching_freq = 28500  # 28.5 kHz
# ==========================================

# Load data directly from the sheets inside the Excel files
for t_key, t_info in transformer_map.items():
    data[t_key] = {}
    filepath = os.path.join(script_dir, f"{t_key}_characteristics.xlsx")
    
    if not os.path.exists(filepath):
        print(f"ERROR: Could not find the Excel file: {filepath}")
        sys.exit(1)
        
    print(f"Opening {t_key}_characteristics.xlsx (Labeling as {t_info['name']})...")
    
    for test in tests:
        data[t_key][test] = pd.read_excel(filepath, sheet_name=test)
        print(f"  -> Successfully loaded sheet: {test}")

print("\nAll data loaded! Calculating parameters...")

# Calculate parameters at 28-30kHz
results = []
for t_key, t_info in transformer_map.items():
    df_open = data[t_key]['meas12open34']
    df_short = data[t_key]['meas12short34']
    
    mask_open = (df_open['Frequency'] >= 28000) & (df_open['Frequency'] <= 30000)
    mask_short = (df_short['Frequency'] >= 28000) & (df_short['Frequency'] <= 30000)
    
    Lp_open_H = df_open.loc[mask_open, 'Lp'].mean()
    Ls_short_H = df_short.loc[mask_short, 'Ls'].mean()
    
    k = np.sqrt(1 - (Ls_short_H / Lp_open_H))
    Lm_H = (k**2) * Lp_open_H
    
    results.append({
        'Transformer': t_info['name'], 
        'k': k, 
        'Lm (uH)': Lm_H * 1e6, 
        'Lp_open (uH)': Lp_open_H * 1e6, 
        'Ls_short (uH)': Ls_short_H * 1e6
    })

res_df = pd.DataFrame(results)
res_df.to_csv(os.path.join(script_dir, "calculated_parameters_28_30kHz_uH.csv"), index=False)
print("\n--- Calculated Parameters at 28-30 kHz ---")
print(res_df.to_string())


# --- Helper Function for Formatting Plots ---
def format_and_save_plot(ax, ylabel, filename):
    ax.set_xscale('log')
    ax.set_xlim(x_axis_min, x_axis_max)
    
    # Format y-axis to prevent scientific notation if needed
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:g}'))
    
    ax.set_xlabel('Frequency (Hz)', fontsize=20)
    ax.set_ylabel(ylabel, fontsize=20)
    
    # Grid matching your exact style preference
    ax.grid(True, which="both", ls="--", linewidth=1.0)
    ax.tick_params(axis='both', which='major', labelsize=17)
    
    # Legend settings
    legend = ax.legend(fontsize=15, loc='upper left')
    if legend:
        legend.get_frame().set_alpha(0.95)
        
    plt.tight_layout()
    plt.savefig(os.path.join(script_dir, filename), format='pdf', bbox_inches='tight')
    plt.close()


# Plot 1: Magnetizing Inductance (Lp converted to uH)
fig, ax = plt.subplots(figsize=(5, 5))
for t_key, t_info in transformer_map.items():
    df = data[t_key]['meas12open34']
    x_val = df['Frequency'].values
    y_val = df['Lp'].values * 1e6
    ax.plot(x_val, y_val, label=f"{t_info['name']}", color=t_info['color'], 
            linestyle=t_info['linestyle'], linewidth=t_info['linewidth'], alpha=t_info['alpha'])
    
    # Mark the dot at 28.5 kHz and annotate
    y_point = np.interp(switching_freq, x_val, y_val)
    ax.plot(switching_freq, y_point, marker='o', markersize=8, color=t_info['color'], markeredgecolor='white', markeredgewidth=1.5, linestyle='None')
    ax.annotate('28.5 kHz', xy=(switching_freq, y_point), xytext=(10, 0), textcoords='offset points', color='black', fontsize=12, va='center')
format_and_save_plot(ax, 'Magnetizing Inductance (uH)', "magnetizing_inductance_uH.pdf")

# Plot 2: Rs for Short Circuit Tests (Converted to mOhm, linear scale)
fig, ax = plt.subplots(figsize=(8, 6))
for t_key, t_info in transformer_map.items():
    df_p = data[t_key]['meas12short34']
    x_val = df_p['Frequency'].values
    y_val = df_p['Rs'].values * 1000
    ax.plot(x_val, y_val, label=f"{t_info['name']}", color=t_info['color'], 
            linestyle=t_info['linestyle'], linewidth=t_info['linewidth'], alpha=t_info['alpha'])
    
    # Mark the dot at 28.5 kHz and annotate
    y_point = np.interp(switching_freq, x_val, y_val)
    ax.plot(switching_freq, y_point, marker='o', markersize=8, color=t_info['color'], markeredgecolor='white', markeredgewidth=1.5, linestyle='None')
    ax.annotate('28.5 kHz', xy=(switching_freq, y_point), xytext=(-50, 5), textcoords='offset points', color='black', fontsize=12, va='center')
format_and_save_plot(ax, 'AC Resistance (mΩ)', "rs_short_circuit.pdf")

# Plot 3: Leakage Inductance (Primary Only, Ls converted to uH)
fig, ax = plt.subplots(figsize=(8, 6))
for t_key, t_info in transformer_map.items():
    df_p = data[t_key]['meas12short34']
    x_val = df_p['Frequency'].values
    y_val = df_p['Ls'].values * 1e6
    ax.plot(x_val, y_val, label=f"{t_info['name']}", color=t_info['color'], 
            linestyle=t_info['linestyle'], linewidth=t_info['linewidth'], alpha=t_info['alpha'])
    
    # Mark the dot at 28.5 kHz and annotate
    y_point = np.interp(switching_freq, x_val, y_val)
    ax.plot(switching_freq, y_point, marker='o', markersize=8, color=t_info['color'], markeredgecolor='white', markeredgewidth=1.5, linestyle='None')
format_and_save_plot(ax, 'Leakage Inductance (uH)', "leakage_inductance_uH.pdf")

# Plot 4: Rs for Open Circuit Tests (Converted to mOhm, linear scale)
fig, ax = plt.subplots(figsize=(8, 6))
for t_key, t_info in transformer_map.items():
    df_p = data[t_key]['meas12open34']
    x_val = df_p['Frequency'].values
    y_val = df_p['Rs'].values * 1000
    ax.plot(x_val, y_val, label=f"{t_info['name']}", color=t_info['color'], 
            linestyle=t_info['linestyle'], linewidth=t_info['linewidth'], alpha=t_info['alpha'])
    
    # Mark the dot at 28.5 kHz and annotate
    y_point = np.interp(switching_freq, x_val, y_val)
    ax.plot(switching_freq, y_point, marker='o', markersize=8, color=t_info['color'], markeredgecolor='white', markeredgewidth=1.5, linestyle='None')
    ax.annotate('28.5 kHz', xy=(switching_freq, y_point), xytext=(10, 0), textcoords='offset points', color='black', fontsize=12, va='center')
format_and_save_plot(ax, 'AC Resistance (mΩ)', "rs_open_circuit.pdf")

print("\nPDF Plots generated successfully in your folder!")