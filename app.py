"""
Interactive Beam Lab — Light Engineering Edition
Clean white theme with steel-blue, crimson and amber accents.
Tabs: 1. Structure  2. Reactions  3. Shear Force  4. Bending Moment  5. Deflection
"""

import streamlit as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from anastruct import SystemElements

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Beam Lab",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS — Light theme
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=DM+Sans:wght@400;500;700&family=DM+Serif+Display&display=swap');

:root {
    --bg:        #f5f7fa;
    --surface:   #ffffff;
    --surface2:  #eef1f6;
    --border:    #d0d7e3;
    --blue:      #1b4f8a;
    --blue-lt:   #2d7dd2;
    --crimson:   #c0392b;
    --amber:     #d97706;
    --green:     #0a7a55;
    --text:      #1a202c;
    --text-dim:  #6b7a99;
    --mono:      'JetBrains Mono', monospace;
    --sans:      'DM Sans', sans-serif;
    --serif:     'DM Serif Display', serif;
}

/* ── Shell ── */
.stApp {
    background-color: var(--bg) !important;
    font-family: var(--sans);
    color: var(--text);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] label {
    font-family: var(--mono) !important;
    font-size: 0.72rem !important;
    color: var(--blue) !important;
    letter-spacing: 0.04em !important;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-top: 3px solid var(--blue) !important;
    border-radius: 6px !important;
    padding: 14px 16px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
}
[data-testid="metric-container"] label {
    font-family: var(--mono) !important;
    font-size: 0.66rem !important;
    color: var(--blue) !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: var(--mono) !important;
    font-size: 0.95rem !important;
    color: var(--text) !important;
    font-weight: 600 !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 2px solid var(--border) !important;
    gap: 0;
    background: var(--surface2);
    border-radius: 8px 8px 0 0;
    padding: 6px 8px 0;
}
[data-testid="stTabs"] button[role="tab"] {
    font-family: var(--mono) !important;
    font-size: 0.73rem !important;
    color: var(--text-dim) !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    padding: 8px 18px !important;
    letter-spacing: 0.05em;
    margin-bottom: -2px;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: var(--blue) !important;
    border-bottom: 2px solid var(--blue) !important;
    background: transparent !important;
    font-weight: 600 !important;
}
[data-testid="stTabs"] [role="tabpanel"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-top: none;
    border-radius: 0 0 8px 8px;
    padding: 20px !important;
}

/* ── Tables ── */
thead th {
    background: var(--surface2) !important;
    color: var(--blue) !important;
    font-family: var(--mono) !important;
    font-size: 0.73rem !important;
    border-bottom: 2px solid var(--border) !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
tbody td {
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 0.84rem !important;
    border-bottom: 1px solid var(--border) !important;
}
table {
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    overflow: hidden;
}

/* ── Inputs ── */
[data-baseweb="select"] > div,
[data-baseweb="input"] > div {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    font-family: var(--mono) !important;
    font-size: 0.84rem !important;
}
[data-testid="stRadio"] label {
    font-family: var(--mono) !important;
    font-size: 0.8rem !important;
}

/* ── Misc ── */
hr { border-color: var(--border) !important; }
.stCaption, small { color: var(--text-dim) !important; font-family: var(--mono) !important; }

/* ── Banner ── */
.beam-banner {
    display: flex; align-items: center; gap: 20px;
    padding: 18px 28px;
    background: linear-gradient(135deg, #1b4f8a 0%, #2d7dd2 100%);
    border-radius: 10px;
    margin-bottom: 22px;
    box-shadow: 0 4px 18px rgba(27,79,138,0.18);
}
.beam-banner-title {
    font-family: 'DM Serif Display', serif;
    color: #ffffff;
    font-size: 1.7rem;
    letter-spacing: 0.02em;
    line-height: 1;
}
.beam-banner-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: rgba(255,255,255,0.68);
    margin-top: 5px;
}
.badge {
    font-family: var(--mono); font-size: 0.63rem;
    background: rgba(255,255,255,0.18);
    color: #fff; padding: 3px 10px;
    border-radius: 20px; letter-spacing: 0.1em;
    border: 1px solid rgba(255,255,255,0.3);
}

/* ── Sidebar section headers ── */
.sidebar-section {
    font-family: var(--mono);
    font-size: 0.62rem;
    color: var(--blue);
    letter-spacing: 0.16em;
    text-transform: uppercase;
    border-bottom: 1px solid var(--border);
    padding-bottom: 5px;
    margin: 18px 0 10px 0;
}

/* ── Service badge ── */
.svc-pass {
    background: #d1fae5; color: #065f46;
    border: 1px solid #6ee7b7;
    font-family: var(--mono); font-size: 0.82rem;
    padding: 10px 18px; border-radius: 6px;
    margin-top: 14px;
}
.svc-fail {
    background: #fee2e2; color: #7f1d1d;
    border: 1px solid #fca5a5;
    font-family: var(--mono); font-size: 0.82rem;
    padding: 10px 18px; border-radius: 6px;
    margin-top: 14px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="beam-banner">
  <div style="font-size:2rem">🏗</div>
  <div>
    <div class="beam-banner-title">Beam Lab</div>
    <div class="beam-banner-sub">2D Elastic Analysis &nbsp;·&nbsp; Direct Stiffness Method &nbsp;·&nbsp; IS 800 : 2007</div>
  </div>
  <div style="margin-left:auto;display:flex;gap:8px;align-items:center">
    <span class="badge">v2.1</span>
    <span class="badge">anaStruct</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MATPLOTLIB LIGHT THEME
# ─────────────────────────────────────────────────────────────────────────────
PLOT_BG  = "#ffffff"
PLOT_AX  = "#f8f9fc"
BLUE     = "#1b4f8a"
BLUE_LT  = "#2d7dd2"
CRIMSON  = "#c0392b"
AMBER    = "#d97706"
GREEN    = "#0a7a55"
TEXT_C   = "#1a202c"
GRID_C   = "#dde3ef"
DIM_C    = "#9aaabf"

def style_ax(ax, title=""):
    ax.set_facecolor(PLOT_AX)
    ax.tick_params(colors=TEXT_C, labelsize=8.5)
    ax.xaxis.label.set_color(TEXT_C)
    ax.yaxis.label.set_color(TEXT_C)
    ax.xaxis.label.set_fontfamily("monospace")
    ax.yaxis.label.set_fontfamily("monospace")
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_C)
    ax.grid(True, color=GRID_C, linewidth=0.6, linestyle="-", alpha=1.0)
    ax.set_axisbelow(True)
    if title:
        ax.set_title(title, color=BLUE, fontsize=10,
                     fontfamily="monospace", pad=10, fontweight="bold")

def make_fig(h=3.8):
    fig, ax = plt.subplots(figsize=(11, h))
    fig.patch.set_facecolor(PLOT_BG)
    return fig, ax

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-section">📐 Geometry</div>', unsafe_allow_html=True)
    L = st.slider("Beam Length (m)", 1, 20, 10)
    N_ELEM = 40

    st.markdown('<div class="sidebar-section">🔩 Material & Section</div>', unsafe_allow_html=True)
    E_GPa = st.number_input("E  (GPa)", value=200.0, step=10.0, min_value=1.0)
    I_cm4 = st.number_input("I  (cm⁴)", value=33000.0, step=500.0, min_value=1.0)
    E  = E_GPa * 1e6
    I  = I_cm4 * 1e-8
    EA = E * 1e-2

    st.markdown('<div class="sidebar-section">⬇ Loads</div>', unsafe_allow_html=True)
    load_type = st.radio("Load Type", ["Point Load", "UDL", "Both"])

    P, x_load, q = 0.0, float(L) / 2, 0.0
    if load_type in ("Point Load", "Both"):
        P      = st.slider("Point Load P (kN)", -200, 200, -50)
        x_load = st.slider("Position a (m)", 0.0, float(L), float(L) / 2, step=0.25)
    if load_type in ("UDL", "Both"):
        q = st.slider("UDL w (kN/m)", -50, 50, -10)

    st.markdown('<div class="sidebar-section">🔧 Supports</div>', unsafe_allow_html=True)
    left_support  = st.selectbox("Left",  ["Pinned", "Fixed", "Free"])
    right_support = st.selectbox("Right", ["Pinned", "Fixed", "Roller (vertical)"])

# ─────────────────────────────────────────────────────────────────────────────
# ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
def apply_support(ss, node_id, stype):
    if stype == "Pinned":               ss.add_support_hinged(node_id=node_id)
    elif stype == "Fixed":              ss.add_support_fixed(node_id=node_id)
    elif stype == "Roller (vertical)":  ss.add_support_roll(node_id=node_id, direction=2)

@st.cache_data(show_spinner=False)
def run_analysis(L, E, I, EA, P, x_load, q, ls, rs, N, load_type):
    ss = SystemElements(EI=E * I, EA=EA)
    ss.add_multiple_elements([[0, 0], [L, 0]], n=N)
    apply_support(ss, 1,     ls)
    apply_support(ss, N + 1, rs)
    if load_type in ("Point Load", "Both") and P != 0:
        frac = np.clip(x_load / L, 0, 1)
        nid  = max(1, min(N + 1, round(frac * N) + 1))
        ss.point_load(node_id=nid, Fy=P)
    if load_type in ("UDL", "Both") and q != 0:
        for eid in range(1, N + 1):
            ss.q_load(q=q, element_id=eid)
    ss.solve()
    return ss

try:
    with st.spinner("Solving…"):
        ss = run_analysis(L, E, I, EA, P, x_load, q,
                          left_support, right_support, N_ELEM, load_type)
    solved = True
except Exception as exc:
    solved = False
    st.error(f"⚠️  Analysis failed — check boundary conditions.\n\n`{exc}`")

# ─────────────────────────────────────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────────────────────────────────────
if solved:
    react = ss.reaction_forces
    nodes = ss.node_map

    def rxn(nid, attr):
        n = react.get(nid)
        return getattr(n, attr, 0.0) if n is not None else 0.0

    R_lV = rxn(1,          "Fy");   R_rV = rxn(N_ELEM + 1, "Fy")
    R_lH = rxn(1,          "Fx");   R_lM = rxn(1,           "Mz")
    R_rM = rxn(N_ELEM + 1, "Mz")
    max_def_mm = max(abs(n.uy) * 1e3 for n in nodes.values()) if nodes else 0.0
    max_def_m  = max_def_mm / 1e3

    # ── KPI strip ────────────────────────────────────────────────────────────
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("↕  R_left",   f"{R_lV:+.2f} kN")
    k2.metric("↕  R_right",  f"{R_rV:+.2f} kN")
    k3.metric("⟳  M_left",   f"{R_lM:+.2f} kN·m")
    k4.metric("⟳  M_right",  f"{R_rM:+.2f} kN·m")
    k5.metric("⬇  δ_max",    f"{max_def_mm:.2f} mm")

    st.markdown("<div style='margin:16px 0'></div>", unsafe_allow_html=True)

    # ── Collect diagram data ──────────────────────────────────────────────────
    x_pts, shear_vals, moment_vals, defl_vals = [], [], [], []
    for eid, el in ss.element_map.items():
        x_pts      += [el.vertex_1.x, el.vertex_2.x]
        shear_vals  += [el.shear_force[0],    el.shear_force[-1]]
        moment_vals += [el.bending_moment[0], el.bending_moment[-1]]
        defl_vals   += [
            ss.node_map[el.node_id1].uy * 1e3,
            ss.node_map[el.node_id2].uy * 1e3,
        ]
    order = np.argsort(x_pts)
    xs = np.array(x_pts)[order]
    Vs = np.array(shear_vals)[order]
    Ms = np.array(moment_vals)[order]
    Ds = np.array(defl_vals)[order]

    # ── Annotate peak helper ──────────────────────────────────────────────────
    def annotate_peak(ax, xs, ys, color, unit):
        i    = int(np.argmax(np.abs(ys)))
        sign = 1 if ys[i] >= 0 else -1
        yspan = np.ptp(ys) if np.ptp(ys) > 0 else 1
        offset = ys[i] - sign * yspan * 0.32
        ax.annotate(
            f" {ys[i]:.2f} {unit}",
            xy=(xs[i], ys[i]),
            xytext=(xs[i], offset),
            color=color, fontsize=9, fontfamily="monospace",
            ha="center", fontweight="bold",
            arrowprops=dict(arrowstyle="-|>", color=color, lw=1.0),
        )

    # ─────────────────────────────────────────────────────────────────────────
    # TABS  (order: Structure · Reactions · Shear · Moment · Deflection)
    # ─────────────────────────────────────────────────────────────────────────
    tab_str, tab_rxn, tab_sfd, tab_bmd, tab_def, tab_comb = st.tabs([
        "🏗  Structure",
        "📋  Reactions",
        "⚡  Shear Force",
        "🌀  Bending Moment",
        "🔽  Deflection",
        "Combined Diagram"
    ])

    # ── 1. STRUCTURE ──────────────────────────────────────────────────────────
    with tab_str:
        fig, ax = make_fig(h=4.2)

        # Beam
        ax.plot([0, L], [0, 0], color=BLUE, linewidth=7,
                solid_capstyle="round", zorder=3)

        def draw_pinned(ax, x):
            tri = plt.Polygon(
                [[x, 0], [x - 0.38*L/10, -0.45], [x + 0.38*L/10, -0.45]],
                closed=True, color=AMBER, zorder=4, alpha=0.95)
            ax.add_patch(tri)
            ax.plot([x - 0.5*L/10, x + 0.5*L/10], [-0.52, -0.52],
                    color=AMBER, lw=2)

        def draw_fixed(ax, x, side="left"):
            s = -1 if side == "left" else 1
            for y in np.linspace(-0.55, 0.55, 8):
                ax.plot([x, x + s * 0.32*L/10],
                        [y, y + s * 0.18],
                        color=AMBER, lw=1.3, alpha=0.75)
            ax.plot([x, x], [-0.6, 0.6], color=AMBER, lw=3)

        def draw_roller(ax, x):
            c = plt.Circle((x, -0.3), 0.16*L/10, color=AMBER, zorder=4)
            ax.add_patch(c)
            ax.plot([x - 0.5*L/10, x + 0.5*L/10], [-0.48, -0.48],
                    color=AMBER, lw=2)

        if left_support == "Pinned":               draw_pinned(ax, 0)
        elif left_support == "Fixed":              draw_fixed(ax, 0, "left")
        if right_support == "Pinned":              draw_pinned(ax, L)
        elif right_support == "Fixed":             draw_fixed(ax, L, "right")
        elif right_support == "Roller (vertical)": draw_roller(ax, L)

        # Point load arrow
        if load_type in ("Point Load", "Both") and P != 0:
            d = -1 if P < 0 else 1
            ax.annotate("", xy=(x_load, 0.05*d), xytext=(x_load, d * 1.0),
                arrowprops=dict(arrowstyle="-|>", color=CRIMSON, lw=2.4,
                                mutation_scale=22))
            ax.text(x_load, d * 1.15, f"P = {P} kN", ha="center",
                    va="bottom" if d > 0 else "top",
                    color=CRIMSON, fontsize=9.5, fontfamily="monospace",
                    fontweight="bold")

        # UDL
        if load_type in ("UDL", "Both") and q != 0:
            d = -1 if q < 0 else 1
            xs_udl = np.linspace(0, L, 12)
            for xi in xs_udl:
                ax.annotate("", xy=(xi, 0.05*d), xytext=(xi, d * 0.7),
                    arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.4,
                                    mutation_scale=14))
            ax.plot([0, L], [d * 0.7, d * 0.7],
                    color=GREEN, lw=1.8)
            ax.text(L / 2, d * 0.88, f"w = {q} kN/m", ha="center",
                    color=GREEN, fontsize=9.5, fontfamily="monospace",
                    fontweight="bold")

        # Dimension line
        y_dim = -0.82
        ax.annotate("", xy=(L, y_dim), xytext=(0, y_dim),
            arrowprops=dict(arrowstyle="<->", color=DIM_C, lw=1))
        ax.text(L / 2, y_dim - 0.1, f"L = {L} m", ha="center", va="top",
                color=DIM_C, fontsize=8.5, fontfamily="monospace")

        ax.set_xlim(-0.8, L + 0.8)
        ax.set_ylim(-1.15, 1.45)
        ax.set_xlabel("x  (m)", fontsize=9)
        ax.set_yticks([])
        style_ax(ax, "LOADED STRUCTURE")
        fig.tight_layout(pad=1.5)
        st.pyplot(fig); plt.close(fig)

    # ── 2. REACTIONS ─────────────────────────────────────────────────────────
    with tab_rxn:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### Support Reactions")
            st.table({
                "Location":   ["Left",           "Right"],
                "V  (kN)":    [f"{R_lV:+.2f}",   f"{R_rV:+.2f}"],
                "H  (kN)":    [f"{R_lH:+.2f}",   "—"],
                "M  (kN·m)":  [f"{R_lM:+.2f}",   f"{R_rM:+.2f}"],
            })
        with c2:
            st.markdown("##### Configuration")
            st.table({
                "Parameter": ["L", "E", "I", "Left BC", "Right BC", "Load", "δ_max"],
                "Value":     [f"{L} m", f"{E_GPa} GPa", f"{I_cm4} cm⁴",
                              left_support, right_support, load_type,
                              f"{max_def_mm:.2f} mm"],
            })

        if max_def_m > 0:
            ratio = L / max_def_m
            limit = 300
            ok    = ratio >= limit
            cls   = "svc-pass" if ok else "svc-fail"
            icon  = "✅" if ok else "❌"
            st.markdown(
                f'<div class="{cls}">'
                f'{icon} &nbsp; IS 800 Cl. 5.6.1 Serviceability &nbsp;|&nbsp; '
                f'<b>L / δ = {ratio:.0f}</b> &nbsp;|&nbsp; Limit = L/{limit}'
                f' &nbsp;|&nbsp; <b>{"PASS" if ok else "FAIL"}</b></div>',
                unsafe_allow_html=True,
            )

    # ── 3. SHEAR FORCE ────────────────────────────────────────────────────────
    with tab_sfd:
        fig, ax = make_fig()
        ax.fill_between(xs, Vs, 0, where=(Vs >= 0),
                        color=BLUE_LT, alpha=0.20, interpolate=True)
        ax.fill_between(xs, Vs, 0, where=(Vs <  0),
                        color=CRIMSON, alpha=0.18, interpolate=True)
        ax.plot(xs, Vs, color=BLUE, linewidth=2.2)
        ax.axhline(0, color=GRID_C, linewidth=1)
        ax.set_xlabel("x  (m)"); ax.set_ylabel("V  (kN)")
        style_ax(ax, "SHEAR FORCE DIAGRAM")
        if np.any(Vs != 0):
            annotate_peak(ax, xs, Vs, CRIMSON, "kN")
        fig.tight_layout(pad=1.5)
        st.pyplot(fig); plt.close(fig)

    # ── 4. BENDING MOMENT ────────────────────────────────────────────────────
    with tab_bmd:
        fig, ax = make_fig()
        ax.fill_between(xs, Ms, 0, where=(Ms >= 0),
                        color=AMBER, alpha=0.20, interpolate=True)
        ax.fill_between(xs, Ms, 0, where=(Ms <  0),
                        color=GREEN, alpha=0.18, interpolate=True)
        ax.plot(xs, Ms, color=AMBER, linewidth=2.2)
        ax.axhline(0, color=GRID_C, linewidth=1)
        ax.set_xlabel("x  (m)"); ax.set_ylabel("M  (kN·m)")
        style_ax(ax, "BENDING MOMENT DIAGRAM")
        if np.any(Ms != 0):
            annotate_peak(ax, xs, Ms, BLUE, "kN·m")
        fig.tight_layout(pad=1.5)
        st.pyplot(fig); plt.close(fig)

    # ── 5. DEFLECTION ────────────────────────────────────────────────────────
    with tab_def:
        from scipy.interpolate import CubicSpline

        # Smooth nodal deflections with a cubic spline
        xs_u, ui = np.unique(xs, return_index=True)
        Ds_u     = Ds[ui]
        cs       = CubicSpline(xs_u, Ds_u, bc_type="not-a-knot")
        xs_fine  = np.linspace(xs_u[0], xs_u[-1], 600)
        Ds_fine  = cs(xs_fine)

        # Visual beam half-depth in mm-axis units (10 % of deflection range)
        d_range = max(np.ptp(Ds_fine), 1e-6)
        h_beam  = max(d_range * 0.12, 0.5)

        fig, ax = make_fig(h=4.6)

        # Undeformed beam — light grey filled rectangle
        ax.fill_between(xs_fine, h_beam, -h_beam,
                        color="#e2e8f0", alpha=0.9, zorder=1)
        ax.plot(xs_fine,  np.full_like(xs_fine,  h_beam), color=DIM_C, lw=1.0, zorder=2)
        ax.plot(xs_fine,  np.full_like(xs_fine, -h_beam), color=DIM_C, lw=1.0, zorder=2)
        ax.plot(xs_fine, np.zeros_like(xs_fine), color=DIM_C,
                lw=0.8, linestyle="--", zorder=2, label="Undeformed centroid")

        # Deflected beam — coloured band following the spline
        top    = Ds_fine + h_beam
        bottom = Ds_fine - h_beam
        ax.fill_between(xs_fine, top, bottom,
                        color=BLUE_LT, alpha=0.28, zorder=3)
        ax.plot(xs_fine, top,    color=BLUE, lw=1.6, zorder=4)
        ax.plot(xs_fine, bottom, color=BLUE, lw=1.6, zorder=4)
        ax.plot(xs_fine, Ds_fine, color=BLUE, lw=2.2, zorder=5,
                linestyle="--", alpha=0.7, label="Deflected centroid")

        # Support verticals
        for xb in [xs_u[0], xs_u[-1]]:
            ax.axvline(xb, color=AMBER, lw=1.4, linestyle=":", zorder=6, alpha=0.65)

        # Peak annotation + drop-line
        if np.any(Ds_fine != 0):
            i_pk  = int(np.argmax(np.abs(Ds_fine)))
            y_pk  = Ds_fine[i_pk]
            x_pk  = xs_fine[i_pk]
            sign  = 1 if y_pk >= 0 else -1
            y_txt = y_pk + sign * d_range * 0.35

            ax.plot([x_pk, x_pk], [0, y_pk],
                    color=CRIMSON, lw=1.1, linestyle=":", zorder=6, alpha=0.8)
            ax.plot(x_pk, 0, marker="v" if y_pk < 0 else "^",
                    color=CRIMSON, ms=8, zorder=7, clip_on=False)
            ax.annotate(
                f"δ_max = {y_pk:.2f} mm",
                xy=(x_pk, y_pk + sign * h_beam * 1.1),
                xytext=(x_pk, y_txt),
                color=CRIMSON, fontsize=9.5, fontfamily="monospace",
                fontweight="bold", ha="center",
                arrowprops=dict(arrowstyle="-|>", color=CRIMSON, lw=1.1),
            )

            # Horizontal dimension: span from support to peak
            y_dim = min(bottom) - d_range * 0.18
            ax.annotate("", xy=(x_pk, y_dim), xytext=(xs_u[0], y_dim),
                arrowprops=dict(arrowstyle="<->", color=DIM_C, lw=1))
            ax.text(x_pk / 2, y_dim - d_range * 0.06,
                    f"a = {x_pk:.2f} m", ha="center", va="top",
                    color=DIM_C, fontsize=8, fontfamily="monospace")

        ax.axhline(0, color=DIM_C, lw=0.8, zorder=2)
        ax.set_xlabel("x  (m)", fontsize=9)
        ax.set_ylabel("δ  (mm)   [exaggerated]", fontsize=9)
        style_ax(ax, "DEFLECTED SHAPE  —  Cubic Spline  |  Exaggerated Scale")

        pad = d_range * 0.55 + h_beam * 2.0
        ax.set_ylim(min(Ds_fine) - pad, max(Ds_fine) + pad)
        ax.set_xlim(xs_u[0] - L * 0.04, xs_u[-1] + L * 0.04)

        leg = ax.legend(fontsize=8.5, facecolor=PLOT_AX, edgecolor=GRID_C,
                        framealpha=1, loc="upper right")
        for t in leg.get_texts(): t.set_color(TEXT_C)
        fig.tight_layout(pad=1.5)
        st.pyplot(fig); plt.close(fig)
        

# ─────────────────────────────────────────────────────────────────────────────
# 6. COMBINED DIAGRAM
# ─────────────────────────────────────────────────────────────────────────────
with tab_comb:
    # Create a figure with 3 vertical subplots sharing the same X-axis
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(11, 12), sharex=True)
    fig.patch.set_facecolor(PLOT_BG)

    # --- SUBPLOT 1: STRUCTURE ---
    ax1.plot([0, L], [0, 0], color=BLUE, linewidth=7, solid_capstyle="round", zorder=3)
    
    # Boundary Conditions
    if left_support == "Pinned":               draw_pinned(ax1, 0)
    elif left_support == "Fixed":              draw_fixed(ax1, 0, "left")
    
    if right_support == "Pinned":              draw_pinned(ax1, L)
    elif right_support == "Fixed":             draw_fixed(ax1, L, "right")
    elif right_support == "Roller (vertical)": draw_roller(ax1, L)

    # Point Load Visualization
    if load_type in ("Point Load", "Both") and P != 0:
        d = -1 if P < 0 else 1
        ax1.annotate("", xy=(x_load, 0.05*d), xytext=(x_load, d * 1.0),
                    arrowprops=dict(arrowstyle="-|>", color=CRIMSON, lw=2.4, mutation_scale=22))
        ax1.text(x_load, d * 1.15, f"P={P}kN", ha="center", color=CRIMSON, 
                 fontsize=9, fontfamily="monospace", fontweight="bold")

    # UDL Visualization (Fixed ax variable bug)
    if load_type in ("UDL", "Both") and q != 0:
        d = -1 if q < 0 else 1
        xs_udl = np.linspace(0, L, 12)
        for xi in xs_udl:
            ax1.annotate("", xy=(xi, 0.05*d), xytext=(xi, d * 0.7),
                        arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.4, mutation_scale=14))
        ax1.plot([0, L], [d * 0.7, d * 0.7], color=GREEN, lw=1.8)
        ax1.text(L / 2, d * 0.88, f"w={q}kN/m", ha="center", color=GREEN, 
                 fontsize=9, fontfamily="monospace", fontweight="bold")

    style_ax(ax1, "LOADED STRUCTURE")
    ax1.set_ylim(-1.2, 1.5)
    ax1.get_yaxis().set_visible(False) # Hide Y-axis for cleaner structure view

    # --- SUBPLOT 2: SHEAR FORCE ---
    ax2.fill_between(xs, Vs, 0, where=(Vs >= 0), color=BLUE_LT, alpha=0.20, interpolate=True)
    ax2.fill_between(xs, Vs, 0, where=(Vs < 0), color=CRIMSON, alpha=0.18, interpolate=True)
    ax2.plot(xs, Vs, color=BLUE, linewidth=2)
    ax2.axhline(0, color=GRID_C, linewidth=1)
    style_ax(ax2, "SHEAR FORCE (kN)")
    if np.any(Vs != 0):
        annotate_peak(ax2, xs, Vs, CRIMSON, "kN")

    # --- SUBPLOT 3: BENDING MOMENT ---
    ax3.fill_between(xs, Ms, 0, where=(Ms >= 0), color=AMBER, alpha=0.20, interpolate=True)
    ax3.fill_between(xs, Ms, 0, where=(Ms < 0), color=GREEN, alpha=0.18, interpolate=True)
    ax3.plot(xs, Ms, color=AMBER, linewidth=2)
    ax3.axhline(0, color=GRID_C, linewidth=1)
    style_ax(ax3, "BENDING MOMENT (kN·m)")
    if np.any(Ms != 0):
        annotate_peak(ax3, xs, Ms, BLUE, "kN·m")

    ax3.set_xlabel("Span (m)")
    
    # Final layout adjustments
    fig.tight_layout(pad=3.0)
    st.pyplot(fig)
    plt.close(fig)
# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:32px;padding:12px 0;border-top:1px solid #d0d7e3;
     font-family:'JetBrains Mono',monospace;font-size:0.67rem;color:#9aaabf;
     display:flex;justify-content:space-between">
  <span>🏗 Beam Lab &nbsp;·&nbsp; Direct Stiffness Method &nbsp;·&nbsp; anaStruct engine</span>
  <span>IS 800 : 2007 &nbsp;·&nbsp; IS 456 : 2000</span>
</div>
""", unsafe_allow_html=True)
