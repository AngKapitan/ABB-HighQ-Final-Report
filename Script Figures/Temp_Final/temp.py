import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# Forces Python to look in the exact folder where this script is saved
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- Set Global Plotting Style ---
plt.style.use('seaborn-v0_8-whitegrid')

# 1. Set global standard text to Arial
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams.update({'font.size': 18})

# 2. CRITICAL FIX: Force the math text engine (for $T_{wind}$ etc.) to use Arial
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Arial'
plt.rcParams['mathtext.it'] = 'Arial:italic'
plt.rcParams['mathtext.bf'] = 'Arial:bold'

def process_thermal_data(file_path, max_minutes=None):
    df = pd.read_csv(file_path, encoding='ISO-8859-1', skiprows=29)
    df = df.iloc[1:].reset_index(drop=True)
    df.columns = df.columns.str.strip()
    
    temp_cols = [col for col in df.columns if 'CH' in col]
    for col in temp_cols:
        # Convert to numeric without the rolling average
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(r'\+', '', regex=True).str.strip(), errors='coerce')
        
    time_minutes = np.arange(len(df)) * 0.2 / 60.0
    
    # Filter data to the specified max time limit
    if max_minutes is not None:
        mask = time_minutes <= max_minutes
        df = df[mask]
        time_minutes = time_minutes[mask]
        
    return time_minutes, df

# 1. Load the data with specific time limits
time_E2_nat, df_E2_nat = process_thermal_data('E2_Natural.CSV', max_minutes=60)
time_F2_nat, df_F2_nat = process_thermal_data('F2_Natural.CSV', max_minutes=60)
time_E2_cool, df_E2_cool = process_thermal_data('E2_Cooling.CSV', max_minutes=45)
time_F2_cool, df_F2_cool = process_thermal_data('F2_Cooling.CSV', max_minutes=45)

# 2. Define the exact sensor mappings
labels_E2 = {
    'CH1': r'$T_{\mathrm{top, in}}$',
    'CH2': r'$T_{\mathrm{Al}}$',
    'CH3': r'$T_{\mathrm{left, in}}$',
    'CH5': r'$T_{\mathrm{wind}}$',
    'CH6': r'$T_{\mathrm{bot, out}}$',
    'CH7': r'$T_{\mathrm{left, out}}$',
    'CH8': r'$T_{\mathrm{top, out}}$'
}

labels_F2 = {
    'CH1': r'$T_{\mathrm{top, in}}$',
    'CH2': r'$T_{\mathrm{Al}}$',
    'CH3': r'$T_{\mathrm{wind}}$',
    'CH4': r'$T_{\mathrm{left, in}}$',
    'CH6': r'$T_{\mathrm{bot, out}}$',
    'CH7': r'$T_{\mathrm{left, out}}$',
    'CH8': r'$T_{\mathrm{top, out}}$'
}

# 3. Create a master color dictionary
color_map = {
    r'$T_{\mathrm{wind}}$':       '#d62728',  # Red
    r'$T_{\mathrm{top, in}}$':    '#1f77b4',  # Blue
    r'$T_{\mathrm{left, in}}$':   '#ff7f0e',  # Orange
    r'$T_{\mathrm{Al}}$':         '#2ca02c',  # Green
    r'$T_{\mathrm{top, out}}$':   '#9467bd',  # Purple
    r'$T_{\mathrm{left, out}}$':  '#8c564b',  # Brown
    r'$T_{\mathrm{bot, out}}$':   '#e377c2'   # Pink
}

# 4. Define the exact order and headers for the legend
legend_order = [
    '--- Inside ---',
    r'$T_{\mathrm{wind}}$',
    r'$T_{\mathrm{top, in}}$',
    r'$T_{\mathrm{left, in}}$',
    '--- Outside ---',
    r'$T_{\mathrm{Al}}$',
    r'$T_{\mathrm{top, out}}$',
    r'$T_{\mathrm{left, out}}$',
    r'$T_{\mathrm{bot, out}}$'
]

# --- HARDCODED TEMPERATURE VALUES ---
vals_E2_nat = {
    r'$T_{\mathrm{wind}}$': 74.3,
    r'$T_{\mathrm{top, in}}$': 73.5,
    r'$T_{\mathrm{left, in}}$': 73.0,
    r'$T_{\mathrm{Al}}$': 68.5,
    r'$T_{\mathrm{top, out}}$': 65.3,
    r'$T_{\mathrm{left, out}}$': 60.9,
    r'$T_{\mathrm{bot, out}}$': 67.2
}

vals_F2_nat = {
    r'$T_{\mathrm{wind}}$': 66.7,
    r'$T_{\mathrm{top, in}}$': 65.9,
    r'$T_{\mathrm{left, in}}$': 65.4,
    r'$T_{\mathrm{Al}}$': 61.5,
    r'$T_{\mathrm{top, out}}$': 62.6,
    r'$T_{\mathrm{left, out}}$': 58.0,
    r'$T_{\mathrm{bot, out}}$': 63.0
}

vals_E2_cool = {
    r'$T_{\mathrm{wind}}$': 46.5,
    r'$T_{\mathrm{top, in}}$': 43.7,
    r'$T_{\mathrm{left, in}}$': 43.0,
    r'$T_{\mathrm{Al}}$': 40.8,
    r'$T_{\mathrm{top, out}}$': 39.9,
    r'$T_{\mathrm{left, out}}$': 36.5,
    r'$T_{\mathrm{bot, out}}$': 31.1
}

vals_F2_cool = {
    r'$T_{\mathrm{wind}}$': 41.5,
    r'$T_{\mathrm{top, in}}$': 41.7,
    r'$T_{\mathrm{left, in}}$': 40.3,
    r'$T_{\mathrm{Al}}$': 38.1,
    r'$T_{\mathrm{top, out}}$': 40.2,
    r'$T_{\mathrm{left, out}}$': 36.0,
    r'$T_{\mathrm{bot, out}}$': 31.3
}

# --- Helper Functions for Formatting Subplots ---
def format_axis(ax, title_text, bottom_label, xlim, ylim, box_header, hardcoded_vals, box_loc='top left'):
    """Applies formatting, text boxes with hardcoded values, and bottom labels."""
    # Put the main title at the top, bolded
    ax.set_title(title_text, fontsize=18, fontweight='bold', fontname='Arial', pad=15)
    
    ax.set_xlabel('Time (Minutes)', fontsize=16, fontname='Arial')
    ax.set_ylabel('Temperature (°C)', fontsize=16, fontname='Arial')
    
    # Put the (a), (b), etc. label at the bottom, centered, NOT bolded
    ax.text(0.5, -0.22, bottom_label, transform=ax.transAxes, ha='center', 
            fontsize=16, fontweight='normal', fontname='Arial')
    
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.grid(True, which="both", ls="--", linewidth=1.0)
    
    # Force tick labels to use Arial
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname('Arial')
        label.set_fontsize(18)
    
    # Build the text block using the provided hardcoded values
    lines = [box_header]
    for item in legend_order:
        if item in hardcoded_vals:
            val = hardcoded_vals[item]
            lines.append(f"{item}: {val:.1f} °C")
            
    text_str = '\n'.join(lines)
    
    # Narrow margin (pad=0.2)
    props = dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9, edgecolor='lightgrey')
    
    # Placement logic
    if box_loc == 'bottom right':
        ax.text(0.985, 0.035, text_str, transform=ax.transAxes, fontsize=12,
                verticalalignment='bottom', horizontalalignment='right', 
                multialignment='left',  # <--- CRITICAL FIX: Aligns text inside the box to the left
                bbox=props, fontname='Arial')
    else:
        ax.text(0.015, 0.985, text_str, transform=ax.transAxes, fontsize=12,
                verticalalignment='top', horizontalalignment='left', 
                multialignment='left',  # <--- CRITICAL FIX: Aligns text inside the box to the left
                bbox=props, fontname='Arial')

def add_row_legend(ax):
    """Extracts lines from a provided axis and builds a right-aligned legend for that row."""
    handles, labels = ax.get_legend_handles_labels()
    handle_dict = dict(zip(labels, handles))
    blank_handle = mlines.Line2D([], [], color='none')
    
    ordered_handles = []
    ordered_labels = []
    
    for item in legend_order:
        if item.startswith('---'):
            ordered_handles.append(blank_handle)
            ordered_labels.append(item)
        elif item in handle_dict:
            ordered_handles.append(handle_dict[item])
            ordered_labels.append(item)
            
    # Anchor the legend outside the right edge of this specific subplot
    legend = ax.legend(ordered_handles, ordered_labels, loc='center left', bbox_to_anchor=(1.03, 0.5), 
                       prop={'family': 'Arial', 'size': 15}, handlelength=2.5)
    if legend:
        legend.get_frame().set_alpha(0.95)

# ==============================================================================
# --- Figure 1: Master 2x2 Grid ---
# ==============================================================================
fig, axs = plt.subplots(2, 2, figsize=(16, 14))

# --- (a) Top-Left: Edgewise Natural ---
for col, label in labels_E2.items():
    if col in df_E2_nat.columns:
        axs[0, 0].plot(time_E2_nat, df_E2_nat[col], label=label, color=color_map[label], linewidth=1.5, linestyle='-')
format_axis(axs[0, 0], 'Edgewise-wound (Natural Cooling)', '(a)', (0, 60), (20, 75), 
            r'$T$ at 60 min:', vals_E2_nat, box_loc='bottom right')

# --- (b) Top-Right: Flatwise Natural ---
for col, label in labels_F2.items():
    if col in df_F2_nat.columns:
        axs[0, 1].plot(time_F2_nat, df_F2_nat[col], label=label, color=color_map[label], linewidth=1.5, linestyle='-')
format_axis(axs[0, 1], 'Flatwise-wound (Natural Cooling)', '(b)', (0, 60), (20, 75), 
            r'Steady-state $T$:', vals_F2_nat, box_loc='bottom right')

# --- (c) Bottom-Left: Edgewise Forced Air ---
for col, label in labels_E2.items():
    if col in df_E2_cool.columns:
        axs[1, 0].plot(time_E2_cool, df_E2_cool[col], label=label, color=color_map[label], linewidth=1.5, linestyle='-')
format_axis(axs[1, 0], 'Edgewise-wound (Forced Air Cooling)', '(c)', (0, 45), (20, 75), 
            r'Steady-state $T$:', vals_E2_cool)

# --- (d) Bottom-Right: Flatwise Forced Air ---
for col, label in labels_F2.items():
    if col in df_F2_cool.columns:
        axs[1, 1].plot(time_F2_cool, df_F2_cool[col], label=label, color=color_map[label], linewidth=1.5, linestyle='-')
format_axis(axs[1, 1], 'Flatwise-wound (Forced Air Cooling)', '(d)', (0, 45), (20, 75), 
            r'Steady-state $T$:', vals_F2_cool)

# Apply a legend to the right-side plot of the top row, and the right-side plot of the bottom row
add_row_legend(axs[0, 1])
add_row_legend(axs[1, 1])

# Increase horizontal and vertical padding so the bottom labels don't crash into the row below
plt.tight_layout(pad=2.0, h_pad=4.5, w_pad=2.0)

# Save the final master plot
plt.savefig('Combined_Thermal_Comparison.pdf', format='pdf', bbox_inches='tight')
plt.close(fig)

print("Master 2x2 PDF generated with strictly enforced Arial font and left-aligned text boxes.")