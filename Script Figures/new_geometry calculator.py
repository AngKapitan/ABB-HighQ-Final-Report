import math

# --- Constants ---
f_sw = 28.5e3
T_s = 1.0 / f_sw
mu_0 = 4 * math.pi * 1.0e-7
mu_r = 3300.0
V_pri_pk = 100.0
L_m = 200e-6
I_p_rms = 10.0
J = 10 / (0.5 * 4) * 1e6
w_wire = 0.5e-3
h_wire = I_p_rms / (J * w_wire)
d_inter = 0.1e-3
d_left_right = 1e-3
d_upper_down = 1e-3


# --- Helper Functions ---

def _calculate_R_prime_basic(w, l, h, mu_0):
    """Implements Eq. (2.8) from the dissertation."""
    denominator = mu_0 * (w / (2 * l) + (2 / math.pi) * (1 + math.log((math.pi * h) / (4 * l))))
    if denominator == 0:
        return float('inf')
    return 1 / denominator


def _calculate_3d_gap_reluctance(leg_width, core_thickness, gap_length, h_dimension, mu_0):
    """Implements the 3D reluctance methodology from the dissertation."""
    w1, t1 = leg_width, core_thickness
    w2, t2 = core_thickness, leg_width

    # Plane 1
    R_prime_basic_1 = _calculate_R_prime_basic(w=w1, l=gap_length / 2, h=h_dimension, mu_0=mu_0)
    R_prime_total_1 =  R_prime_basic_1
    R_classic_2D_1 = gap_length / (mu_0 * t1)
    sigma_1 = R_prime_total_1 / R_classic_2D_1

    # Plane 2
    R_prime_basic_2 = _calculate_R_prime_basic(w=w2, l=gap_length / 2, h=h_dimension, mu_0=mu_0)
    R_prime_total_2 = R_prime_basic_2
    R_classic_2D_2 = gap_length / (mu_0 * t2)
    sigma_2 = R_prime_total_2 / R_classic_2D_2

    R_classic_3D = gap_length / (mu_0 * leg_width * core_thickness)
    R_gap_3D = sigma_1 * sigma_2 * R_classic_3D
    return R_gap_3D


# --- Main Geometry Function with Bisection on l_cent ---

def calculate_geometry_dissertation_bisection_l_cent(Np, w_cent, l_g):
    """Calculates geometry using 3D reluctance model and bisection on core thickness (l_cent)."""
    w_out = w_cent / 2
    l_window = h_wire + 2 * d_upper_down
    w_window = w_wire * 2 * Np + (2 * Np - 1) * d_inter + 2 * d_left_right
    l_1 = (l_window + w_out - l_g) / 2
    if l_1 <= 0:
        return None

    target_reluctance = Np**2 / L_m

    # Bisection limits for l_cent
    low_l_cent = 0.001  # 1 mm
    high_l_cent = 0.5   # 500 mm

    for _ in range(1000):
        l_cent = (low_l_cent + high_l_cent) / 2
        A_calc = l_cent * w_cent
        h_dim = l_1 - w_cent / 4
        if A_calc <= 0 or h_dim <= 0:
            return None

        # Update MPL using current l_cent
        MPL = 2 * l_window + 2 * w_window + w_cent + math.pi / 8 * 2 * 2 * w_out - 2 * l_g
        R_core = MPL / (mu_0 * mu_r * A_calc)

        R_g_center = _calculate_3d_gap_reluctance(w_cent, l_cent, l_g, h_dim, mu_0)
        R_g_outer = _calculate_3d_gap_reluctance(w_out, l_cent, l_g, h_dim, mu_0)
        R_gap_total = R_g_center + 0.5 * R_g_outer

        total_reluctance = R_core + R_gap_total

        if total_reluctance > target_reluctance:
            low_l_cent = l_cent  # Need more area, so increase thickness
        else:
            high_l_cent = l_cent  # Reluctance too low, reduce thickness

    # Final values
    l_cent_final = (low_l_cent + high_l_cent) / 2
    A_calc_final = l_cent_final * w_cent
    B_act = (V_pri_pk * T_s) / (4 * Np * A_calc_final)

    return {
        "A_calc": A_calc_final,
        "l_cent": l_cent_final,
        "B_act": B_act
    }

# --- Set Parameters and Run ---
results = calculate_geometry_dissertation_bisection_l_cent(Np=8, w_cent=10e-3, l_g=0.1e-3)

# --- Print the final result ---
if results:
    print("Results from Stable Solver:")
    print(f"  Core Thickness (l_cent): {results['l_cent'] * 1000:.2f} mm")
    print(f"  Core Area (A_calc):      {results['A_calc'] * 1e4:.2f} cm^2")
    print(f"  Peak Flux Density (B_act): {results['B_act']:.2f} T")
else:
    print("Calculation failed.")