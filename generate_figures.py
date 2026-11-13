import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('figures', exist_ok=True)

# Set high-quality plotting style
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 9.5,
    'figure.titlesize': 13,
    'figure.dpi': 300,
    'lines.linewidth': 1.8,
    'grid.alpha': 0.4,
    'grid.linestyle': '--'
})

colors = {
    'blue': '#1f77b4',
    'navy': '#0f3b6d',
    'red': '#d62728',
    'crimson': '#8b0000',
    'green': '#2ca02c',
    'darkgreen': '#1b5e20',
    'orange': '#ff7f0e',
    'purple': '#9467bd',
    'gray': '#7f7f7f'
}

# ==============================================================================
# Plot 3: Modulator Characteristic (Table 1: D vs Vc)
# ==============================================================================
def generate_plot3():
    vc_meas = np.array([0.50, 0.60, 0.70, 0.80, 0.90, 1.00])
    d_meas = np.array([28.2, 33.4, 38.4, 43.4, 48.4, 53.8])
    d_pred = vc_meas / 2.0 * 100.0 # ideal: D = Vc / 2V
    
    # Linear regression on measured data
    poly = np.polyfit(vc_meas, d_meas, 1)
    vc_fine = np.linspace(0.45, 1.05, 100)
    d_fit = np.polyval(poly, vc_fine)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 4.2))
    
    # Subplot 1: D vs Vc transfer curve
    ax1.plot(vc_fine, d_fit, color=colors['blue'], label=f'Linear Fit: $D = {poly[0]:.1f}V_C + {poly[1]:.1f}\\%$')
    ax1.plot(vc_meas, d_pred, color='gray', linestyle='--', label=r'Ideal Modulator ($D = V_C / 2\,\mathrm{V}$)')
    ax1.scatter(vc_meas, d_meas, color=colors['navy'], s=50, zorder=5, label='Measured Data (Table 1)')
    ax1.set_xlabel(r'Control Voltage $V_C$ (V)')
    ax1.set_ylabel(r'Measured Duty Cycle $D$ (%)')
    ax1.set_title(r'(a) Modulator Transfer Characteristic')
    ax1.grid(True)
    ax1.legend(loc='lower right', framealpha=0.9)
    ax1.set_xlim(0.45, 1.05)
    ax1.set_ylim(20, 60)
    
    # Subplot 2: Residual Error
    delta_d = d_meas - d_pred
    ax2.bar(vc_meas, delta_d, width=0.04, color=colors['orange'], edgecolor='black', alpha=0.85)
    ax2.axhline(np.mean(delta_d), color='red', linestyle='--', label=f'Mean Offset $= +{np.mean(delta_d):.2f}\\%$ (Delay offset)')
    ax2.set_xlabel(r'Control Voltage $V_C$ (V)')
    ax2.set_ylabel(r'Offset $\Delta D = D_{\mathrm{meas}} - D_{\mathrm{pred}}$ (%)')
    ax2.set_title(r'(b) Modulator Propagation Delay Offset')
    ax2.grid(True, axis='y')
    ax2.legend(loc='upper right', framealpha=0.9)
    ax2.set_xlim(0.45, 1.05)
    ax2.set_ylim(0, 5)
    
    plt.tight_layout()
    plt.savefig('figures/plot3_modulator_char.png')
    plt.close()
    print('Generated plot3_modulator_char.png')

# ==============================================================================
# Plot 4: Closed-Loop Line Regulation (Table 3: Vout & Vc vs Vin)
# ==============================================================================
def generate_plot4():
    vin = np.array([3.0, 3.5, 4.0, 4.5, 5.0])
    vout = np.array([1.181, 1.177, 1.180, 1.175, 1.182])
    vc = np.array([0.831, 0.664, 0.560, 0.542, 0.402])
    
    # Predicted Vc from volt-second balance with Vf = 0.34 V, Vsw = 0.20 V, Vramp = 2.0 V:
    # D = (Vout + Vf)/(Vin - Vsw + Vf) -> Vc_pred = D * 2.0 V
    vc_pred = 2.0 * (1.18 + 0.34) / (vin - 0.20 + 0.34)
    
    fig, ax1 = plt.subplots(figsize=(7.8, 4.2))
    
    color1 = colors['blue']
    ax1.set_xlabel(r'Input Voltage $V_{\mathrm{IN}}$ (V)')
    ax1.set_ylabel(r'Regulated Output Voltage $V_{\mathrm{OUT}}$ (V)', color=color1)
    l1 = ax1.plot(vin, vout, marker='o', color=color1, label=r'Measured $V_{\mathrm{OUT}}$ (DMM)')
    ax1.axhline(1.200, color='gray', linestyle=':', label=r'Design Target $V_{\mathrm{TARGET}} = 1.200\,\mathrm{V}$')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_ylim(1.160, 1.210)
    ax1.grid(True)
    
    ax2 = ax1.twinx()
    color2 = colors['red']
    ax2.set_ylabel(r'Integrator Control Voltage $V_C$ (V)', color=color2)
    l2 = ax2.plot(vin, vc, marker='s', color=color2, label=r'Measured $V_C$')
    l3 = ax2.plot(vin, vc_pred, linestyle='--', color='purple', label=r'Theoretical $V_C = 2.0 \cdot D$')
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.set_ylim(0.30, 0.95)
    
    # Combined legend
    lines = l1 + [ax1.get_lines()[1]] + l2 + l3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='center right', framealpha=0.9, fontsize=9)
    
    plt.title(r'Closed-Loop Line Regulation & Modulator Control Voltage ($R_L = 22\,\Omega$)')
    plt.tight_layout()
    plt.savefig('figures/plot4_line_regulation.png')
    plt.close()
    print('Generated plot4_line_regulation.png')

# ==============================================================================
# Plot 5: Closed-Loop Load Regulation (Table 4)
# ==============================================================================
def generate_plot5():
    # Active loads in CCM
    r_load = np.array([68.0, 47.0, 22.0, 12.0])
    i_load = 1.180 / r_load * 1000.0 # mA: 17.35, 25.11, 53.64, 98.33
    
    vout_3v = np.array([1.183, 1.185, 1.180, 1.181])
    vout_5v = np.array([1.189, 1.188, 1.179, 1.182])
    
    fig, ax = plt.subplots(figsize=(7.8, 4.3))
    
    # Critical boundary for L = 1.0 mH:
    # 3V: Icrit = 4.12 mA; 5V: Icrit = 5.43 mA
    ax.axvspan(0, 5.43, color='orange', alpha=0.15, label=r'DCM Boundary ($I_{\mathrm{LOAD}} < I_{\mathrm{crit}} = 5.43\,\mathrm{mA}$)')
    ax.axvspan(5.43, 110, color='green', alpha=0.08, label=r'CCM Operating Domain ($I_{\mathrm{LOAD}} \geq 17.4\,\mathrm{mA}$)')
    
    ax.plot(i_load, vout_3v, marker='o', color=colors['blue'], label=r'$V_{\mathrm{IN}} = 3.0\,\mathrm{V}$ (Load Reg $= 24.7\,\mathrm{mV/A}$)')
    ax.plot(i_load, vout_5v, marker='s', color=colors['red'], label=r'$V_{\mathrm{IN}} = 5.0\,\mathrm{V}$ (Load Reg $= 86.5\,\mathrm{mV/A}$)')
    
    # Callout for Bleeder Only
    ax.scatter([1.2], [1.18], color='purple', marker='x', s=80, zorder=6)
    ax.annotate(r'Bleeder Only ($1.2\,\mathrm{mA} < I_{\mathrm{crit}}$):' + '\n' + 
                r'$V_{\mathrm{OUT}}(3\mathrm{V}) = 2.869\,\mathrm{V}$' + '\n' +
                r'$V_{\mathrm{OUT}}(5\mathrm{V}) = 4.82\,\mathrm{V}$' + '\n' +
                r'(DCM Runaway, $t_{\mathrm{on,min}} \approx 1.4\,\mu\mathrm{s}$)', 
                xy=(1.2, 1.185), xytext=(8, 1.160),
                bbox=dict(boxstyle="round,pad=0.3", fc="#fdf2f2", ec="red", lw=1),
                arrowprops=dict(arrowstyle="->", color="red"))
                
    ax.set_xlabel(r'Load Current $I_{\mathrm{LOAD}}$ (mA)')
    ax.set_ylabel(r'Output Voltage $V_{\mathrm{OUT}}$ (V)')
    ax.set_title(r'Closed-Loop Load Regulation & Conduction Domains ($L_1 = 1.0\,\mathrm{mH}$)')
    ax.set_xlim(-2, 108)
    ax.set_ylim(1.155, 1.205)
    ax.grid(True)
    ax.legend(loc='lower left', framealpha=0.9, fontsize=8.8)
    
    plt.tight_layout()
    plt.savefig('figures/plot5_load_regulation.png')
    plt.close()
    print('Generated plot5_load_regulation.png')

# ==============================================================================
# Plot 6: Efficiency Comparison: Buck vs Linear (Table 6 & Table 7)
# Single high-clarity plot at 100 mA rated load
# ==============================================================================
def generate_plot6():
    vin = np.array([3.0, 3.5, 4.0, 4.5, 5.0])
    
    # Buck Regulator data at 100 mA (RL = 12 Ohm, Pout = 116.1 mW)
    # Stage efficiency matching loss model: 73.4% at 3V, down to 70.4% at 5V
    eta_buck_pwr = np.array([73.4, 72.5, 71.8, 71.0, 70.4])
    
    # Auxiliary power: P_aux = 132.0 mW (+/-12V for LM741 & LM339)
    # Total efficiency: 116.1 / (Pin_stage + 132 mW)
    p_out = 116.1
    p_in_buck = p_out / (eta_buck_pwr / 100.0)
    p_aux_buck = 132.0
    eta_buck_tot = (p_out / (p_in_buck + p_aux_buck)) * 100.0 # 40.5% down to 39.3%
    
    # Linear Regulator (Exp 8 data)
    eta_lin_pwr = (1.20 / vin) * 100.0 # 40.0% down to 24.0%
    p_aux_lin = 68.0 # single 741
    p_in_lin = vin * 100.0
    eta_lin_tot = (120.0 / (p_in_lin + p_aux_lin)) * 100.0 # 32.6% down to 21.1%
    
    fig, ax = plt.subplots(figsize=(8.0, 4.4))
    
    ax.plot(vin, eta_buck_pwr, marker='o', linewidth=2.2, color=colors['navy'], label=r'Buck: Power Stage Only ($\eta_{\mathrm{stage}} = 73.4\%\dots 70.4\%$)')
    ax.plot(vin, eta_buck_tot, marker='o', linestyle='--', linewidth=2.0, color=colors['blue'], label=r'Buck: Total System ($\eta_{\mathrm{total}} \approx 40.5\%\dots 39.3\%$, incl. $\pm12\,\mathrm{V}$ Aux)')
    ax.plot(vin, eta_lin_pwr, marker='s', linewidth=2.2, color=colors['crimson'], label=r'Linear: Pass Element Only ($V_{\mathrm{OUT}}/V_{\mathrm{IN}} = 40.0\%\dots 24.0\%$)')
    ax.plot(vin, eta_lin_tot, marker='s', linestyle='--', linewidth=2.0, color=colors['red'], label=r'Linear: Total System ($\eta_{\mathrm{total}} = 32.6\%\dots 21.1\%$)')
    
    ax.set_xlabel(r'Input Voltage $V_{\mathrm{IN}}$ (V)')
    ax.set_ylabel(r'Conversion Efficiency $\eta$ (%)')
    ax.set_title(r'Efficiency Comparison: Buck Regulator vs. Linear Regulator ($I_{\mathrm{LOAD}} \approx 100\,\mathrm{mA}$)')
    ax.grid(True)
    ax.legend(loc='center right', fontsize=8.8, framealpha=0.9)
    ax.set_ylim(15, 82)
    ax.set_xlim(2.9, 5.1)
    
    plt.tight_layout()
    plt.savefig('figures/plot6_efficiency_comparison.png')
    plt.close()
    print('Generated plot6_efficiency_comparison.png')

# ==============================================================================
# Plot 7: Loss Budget Breakdown at 5V, 100 mA (Journal Q7)
# ==============================================================================
def generate_plot7():
    # Power Stage Loss Terms at Vin = 5.0V, Iload = 100 mA, Pout = 120 mW
    # D = 0.2857, (1 - D) = 0.7143
    # 1. Schottky diode conduction: (1 - D)*Iload*VF = 0.7143 * 0.10 * 0.47 = 33.57 mW
    # 2. Inductor DCR: Iload^2 * DCR = 0.01 * 0.8 = 8.00 mW
    # 3. Power switch conduction: D * Iload * Vce(sat) (or D*I^2*R) = 4.57 mW
    # 4. Switching loss: 0.5 * Vin * Iload * (tr + tf) * fs = 3.25 mW
    # 5. Gate/base drive loss: 1.00 mW
    # Total Asynchronous Power Stage Loss = 50.39 mW (eta = 70.42%)
    
    categories = ['Diode / Sync\nConduction',
                  r'Inductor' + '\n' + r'DCR Loss' + '\n' + r'($R_L = 0.8\,\Omega$)',
                  'Switch ($Q_3$)\nConduction',
                  r'Switching' + '\n' + r'Loss ($Q_3$)' + '\n' + r'($t_r+t_f=130\,\mathrm{ns}$)',
                  'Drive\nPower']
                  
    losses_asynch = [33.57, 8.00, 4.57, 3.25, 1.00]
    
    # Synchronous Rectification:
    # Replace diode conduction (33.57 mW) with low-side Sync NMOS (Rds = 0.3 Ohm):
    # P_sync_cond = (1 - D) * I^2 * Rds = 0.7143 * 0.01 * 0.3 = 2.14 mW
    # Additional sync gate drive = 1.00 mW
    # Total Synchronous Power Stage Loss = 50.39 - 33.57 + 2.14 + 1.00 = 19.96 mW
    # Synchronous Efficiency = 120 / (120 + 19.96) = 85.74% ~ 85.7%
    losses_synch = [2.14, 8.00, 4.57, 3.25, 2.00] # Drive power includes 1.0 mW main + 1.0 mW sync
    
    x = np.arange(len(categories))
    width = 0.38
    
    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    
    rects1 = ax.bar(x - width/2, losses_asynch, width, label='Asynchronous Buck (1N5817 Schottky)', color=colors['red'], alpha=0.85)
    rects2 = ax.bar(x + width/2, losses_synch, width, label='Synchronous Buck (Active NMOS FET)', color=colors['blue'], alpha=0.85)
    
    for rect in rects1:
        h = rect.get_height()
        ax.annotate(f'{h:.2f} mW', (rect.get_x() + rect.get_width()/2, h),
                    xytext=(0, 4), textcoords="offset points", ha='center', fontsize=8)
    for rect in rects2:
        h = rect.get_height()
        ax.annotate(f'{h:.2f} mW', (rect.get_x() + rect.get_width()/2, h),
                    xytext=(0, 4), textcoords="offset points", ha='center', fontsize=8)
                    
    ax.set_ylabel(r'Power Dissipation (mW)')
    ax.set_title(r'Power Stage Loss Budget at $V_{\mathrm{IN}} = 5.0\,\mathrm{V}$, $I_{\mathrm{LOAD}} = 100\,\mathrm{mA}$ ($P_{\mathrm{OUT}} = 120\,\mathrm{mW}$)')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend(loc='upper right', framealpha=0.9)
    ax.grid(True, axis='y')
    ax.set_ylim(0, 40)
    
    tot_asynch = sum(losses_asynch)
    tot_synch = sum(losses_synch)
    eff_asynch = (120.0 / (120.0 + tot_asynch)) * 100.0
    eff_synch = (120.0 / (120.0 + tot_synch)) * 100.0
    
    textstr = '\n'.join((
        r'$\mathbf{Loss\ Budget\ Summary:}$',
        r'Asynch Total: ' + f'{tot_asynch:.2f} mW ' + r'($\eta = ' + f'{eff_asynch:.1f}' + r'\%$)',
        r'Synch Total: ' + f'{tot_synch:.2f} mW ' + r'($\eta = ' + f'{eff_synch:.1f}' + r'\%$)',
        r'Efficiency Gain: ' + f'+{eff_synch - eff_asynch:.1f}' + r'\% points'
    ))
    props = dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='gray', alpha=0.9)
    ax.text(0.52, 0.65, textstr, transform=ax.transAxes, fontsize=9.5, verticalalignment='top', bbox=props)
    
    plt.tight_layout()
    plt.savefig('figures/plot7_loss_budget.png')
    plt.close()
    print('Generated plot7_loss_budget.png')

if __name__ == '__main__':
    generate_plot3()
    generate_plot4()
    generate_plot5()
    generate_plot6()
    generate_plot7()
    print("All required plots successfully updated.")
