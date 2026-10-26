import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# Forces Python to look in the exact folder where this script is saved
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- Set Global Plotting Style ---
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.serif'] = ['Arial']
plt.rcParams.update({'font.size': 14})




def process_thermal_data(file_path, smooth_window=150):
    df = pd.read_csv(file_path, encoding='ISO-8859-1', skiprows=29)
    df = df.iloc[1:].reset_index(drop=True)
    df.columns = df.columns.str.strip()
    
    temp_cols = [col for col in df.columns if 'CH' in col]
    for col in temp_cols:
        raw_data = pd.to_numeric(df[col].astype(str).str.replace(r'\+', '', regex=True).str.strip(), errors='coerce')
        df[col] = raw_data.rolling(window=smooth_window, min_periods=1).mean()
        
    time_minutes = np.arange(len(df)) * 0.2 / 60.0
    return time_minutes, df

# 1. Load the data
time_E2_nat, df_E2_nat = process_thermal_data('E2_natural.CSV')
time_F2_nat, df_F2_nat = process_thermal_data('F2_natural.CSV')
time_E2_cool, df_E2_cool = process_thermal_data('E2_cooling.CSV')
time_F2_cool, df_F2_cool = process_thermal_data('F2_cooling.CSV')

# 2. Define the exact sensor mappings
labels_E2 = {
    'CH1': r'$T_{\mathrm{top, in}}$',
    'CH2': r'$T_{\mathrm{Al}}$',
    'CH3': r'$T_{\mathrm{left, in}}$',
    'CH4': r'$T_{\mathrm{wind}}$',
    'CH5': r'$T_{\mathrm{top,out_1}}$',
    'CH6': r'$T_{\mathrm{bot, out}}$',
    'CH7': r'$T_{\mathrm{left, out}}$',
    'CH8': r'$T_{\mathrm{top, out_2}}$',
    'CH9': r'$T_{\mathrm{top, out_3}}$',
    'CH10': r'$T_{\mathrm{right, out}}$'
}

labels_F2 = {
    'CH1': r'$T_{\mathrm{top, in}}$',
    'CH2': r'$T_{\mathrm{Al}}$',
    'CH3': r'$T_{\mathrm{wind}}$',
    'CH4': r'$T_{\mathrm{left, in}}$',
    'CH5': r'$T_{\mathrm{top,out_1}}$',
    'CH6': r'$T_{\mathrm{bot, out}}$',
    'CH7': r'$T_{\mathrm{left, out}}$',
    'CH8': r'$T_{\mathrm{top, out_2}}$',
    'CH9': r'$T_{\mathrm{top, out_3}}$',
    'CH10': r'$T_{\mathrm{right, out}}$'
}

# 3. Create a master color dictionary
color_map = {
    r'$T_{\mathrm{wind}}$':       '#d62728',  # Red
    r'$T_{\mathrm{top, in}}$':    '#1f77b4',  # Blue
    r'$T_{\mathrm{left, in}}$':   '#ff7f0e',  # Orange
    r'$T_{\mathrm{Al}}$':         '#2ca02c',  # Green
    r'$T_{\mathrm{top,out_1}}$':  '#9467bd',  # Purple
    r'$T_{\mathrm{top, out_2}}$': '#17becf',  # Cyan
    r'$T_{\mathrm{top, out_3}}$': '#bcbd22',  # Olive
    r'$T_{\mathrm{right, out}}$': '#7f7f7f',  # Gray
    r'$T_{\mathrm{left, out}}$':  '#8c564b',  # Brown
    r'$T_{\mathrm{bot, out}}$':   '#e377c2'   # Pink
}

# 4. Define which curves should be dashed
dashed_labels = [
    r'$T_{\mathrm{Al}}$',
    r'$T_{\mathrm{top,out_1}}$',
    r'$T_{\mathrm{top, out_2}}$',
    r'$T_{\mathrm{top, out_3}}$',
    r'$T_{\mathrm{right, out}}$',
    r'$T_{\mathrm{left, out}}$',
    r'$T_{\mathrm{bot, out}}$'
]

# 5. Define the exact order and headers for the legend
legend_order = [
    '--- Inside ---',
    r'$T_{\mathrm{wind}}$',
    r'$T_{\mathrm{top, in}}$',
    r'$T_{\mathrm{left, in}}$',
    '--- Outside ---',
    r'$T_{\mathrm{Al}}$',
    r'$T_{\mathrm{top,out_1}}$',
    r'$T_{\mathrm{top, out_2}}$',
    r'$T_{\mathrm{top, out_3}}$',
    r'$T_{\mathrm{right, out}}$',
    r'$T_{\mathrm{left, out}}$',
    r'$T_{\mathrm{bot, out}}$'
]

# --- Helper Function for Formatting Plots ---
def format_and_save_plot(ax, xlim, ylim, filename):
    ax.set_xlabel('Time (Minutes)', fontsize=20)
    ax.set_ylabel('Temperature (°C)', fontsize=20)
    
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.grid(True, which="both", ls="-", linewidth=1.0)
    ax.tick_params(axis='both', which='major', labelsize=17)
    
    # Extract existing handles and labels
    handles, labels = ax.get_legend_handles_labels()
    handle_dict = dict(zip(labels, handles))
    
    # Create an invisible handle for the text separators
    blank_handle = mlines.Line2D([], [], color='none')
    
    # Build the final ordered lists for the legend
    ordered_handles = []
    ordered_labels = []
    
    for item in legend_order:
        if item.startswith('---'):
            # It's a header, add the blank handle and the text
            ordered_handles.append(blank_handle)
            ordered_labels.append(item)
        elif item in handle_dict:
            # It's a plot line that exists in this specific chart
            ordered_handles.append(handle_dict[item])
            ordered_labels.append(item)
    
    # Create legend with explicit TNR font and extra handle length for dashes
    legend = ax.legend(ordered_handles, ordered_labels, loc='center left', bbox_to_anchor=(1.02, 0.5), 
                       prop={'family': 'Arial', 'size': 15}, handlelength=2.5)
    
    if legend:
        legend.get_frame().set_alpha(0.95)
        
    plt.tight_layout()
    plt.savefig(filename, format='pdf', bbox_inches='tight')
    plt.close()

# --- Plot 1: Edgewise Natural ---
# Changed figsize to (8, 5) to shorten the graph height to match the legend
fig, ax = plt.subplots(figsize=(8, 4.7))
for col, label in labels_E2.items():
    ls = '-' if label in dashed_labels else '-'
    ax.plot(time_E2_nat, df_E2_nat[col], label=label, color=color_map[label], linewidth=1.0, linestyle=ls)
format_and_save_plot(ax, (0, 240), (20, 80), 'Edgewise_Natural.pdf')

# --- Plot 2: Flatwise Natural ---
fig, ax = plt.subplots(figsize=(8, 4.7))
for col, label in labels_F2.items():
    ls = '-' if label in dashed_labels else '-'
    ax.plot(time_F2_nat, df_F2_nat[col], label=label, color=color_map[label], linewidth=1.0, linestyle=ls)
format_and_save_plot(ax, (0, 240), (20, 80), 'Flatwise_Natural.pdf')

# --- Plot 3: Edgewise Forced-Air ---
fig, ax = plt.subplots(figsize=(8, 4.7))
for col, label in labels_E2.items():
    ls = '-' if label in dashed_labels else '-'
    ax.plot(time_E2_cool, df_E2_cool[col], label=label, color=color_map[label], linewidth=1.0, linestyle=ls)
format_and_save_plot(ax, (0, 240), (20, 80), 'Edgewise_Cooling.pdf')

# --- Plot 4: Flatwise Forced-Air ---
fig, ax = plt.subplots(figsize=(8, 4.7))
for col, label in labels_F2.items():
    ls = '-' if label in dashed_labels else '-'
    ax.plot(time_F2_cool, df_F2_cool[col], label=label, color=color_map[label], linewidth=1.0, linestyle=ls)
format_and_save_plot(ax, (0, 240), (20, 80), 'Flatwise_Cooling.pdf')

print("PDFs generated successfully with shorter graph heights.")