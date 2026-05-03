"""
Interactive Beam Lab — Dark Blueprint Edition
Aesthetic: industrial engineering workstation — dark navy, cyan accents, amber highlights,
blueprint-grid texture, monospace readouts, tight technical typography.
"""

import streamlit as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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
# GLOBAL CSS — Blueprint dark theme
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&family=Orbitron:wght@700&display=swap');

:root {
    --bg:        #080d18;
    --bg2:       #0d1425;
    --bg3:       #111c35;
    --border:    #1e3a5f;
    --cyan:      #00d4ff;
    --cyan-dim:  #0090b0;
    --amber:     #ffaa00;
    --red:       #ff4d6a;
    --green:     #00e5a0;
    --text:      #c8ddf0;
    --text-dim:  #5a7a9a;
    --mono:      'Share Tech Mono', monospace;
    --head:      'Rajdhani', sans-serif;
    --display:   'Orbitron', sans-serif;
}

.stApp {
    background-color: var(--bg);
    background-image:
        linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    color: var(--text);
    font-family: var(--head);
}

[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] label {
    font-family: var(--mono) !important;
    font-size: 0.78rem !important;
    color: var(--cyan) !important;
}

h1, h2, h3 { font-family: var(--display) !important; letter-spacing: 0.06em; }
h1 { color: var(--cyan) !important; font-size: 1.6rem !important; }
h2 { color: var(--amber) !important; font-size: 1.1rem !important; }
h3 { color: var(--text) !important; font-size: 0.95rem !important; }

[data-testid="metric-container"] {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-top: 2px solid var(--cyan) !important;
    border-radius: 4px !important;
    padding: 14px 18px !important;
}
[data-testid="metric-container"] label {
    font-family: var(--mono) !important;
    font-size: 0.68rem !important;
    color: var(--cyan) !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: var(--mono) !important;
    font-size: 1.4rem !important;
    color: #ffffff !important;
}

[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1px solid var(--border) !important;
    gap: 2px;
}
[data-testid="stTabs"] button[role="tab"] {
    font-family: var(--mono) !important;
    font-size: 0.74rem !important;
    color: var(--text-dim) !important;
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 3px 3px 0 0 !important;
    letter-spacing: 0.08em;
    padding: 6px 16px !important;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: var(--cyan) !important;
    border-color: var(--border) var(--border) var(--bg) !important;
    background: var(--bg3) !important;
}

thead th {
    background: var(--bg3) !important;
    color: var(--cyan) !important;
    font-family: var(--mono) !important;
    font-size: 0.74rem !important;
    border-bottom: 1px solid var(--border) !important;
}
tbody td {
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 0.84rem !important;
    border-bottom: 1px solid var(--border) !important;
}
table { border: 1px solid var(--border) !important; }

[data-baseweb="select"] > div,
[data-baseweb="input"] > div {
    background: var(--bg3) !important;
    border-color: var(--border) !important;
    border-radius: 3px !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
}

[data-testid="stRadio"] label {
    font-family: var(--mono) !important;
    font-size: 0.8rem !important;
}

hr { border-color: var(--border) !important; }
.stCaption, small { color: var(--text-dim) !important; font-family: var(--mono) !important; }

.beam-banner {
    display: flex; align-items: center; gap: 16px;
    padding: 16px 24px;
    background: linear-gradient(135deg, #0d1f3c 0%, #091630 100%);
    border: 1px solid var(--border);
    border-left: 4px solid var(--cyan);
    border-radius: 4px;
    margin-bottom: 20px;
}
.beam-banner p { margin: 0; font-family: var(--mono); font-size: 0.74rem; color: var(--text-dim); }
.badge {
    font-family: var(--mono); font-size: 0.64rem;
    background: var(--cyan); color: #000; padding: 2px 8px;
    border-radius: 2px; letter-spacing: 0.1em; font-weight: bold;
}

.sidebar-section {
    font-family: var(--mono);
    font-size: 0.63rem;
    color: var(--cyan);
    letter-spacing: 0.18em;
    text-transform: uppercase;
    border-bottom: 1px solid var(--border);
    padding-bottom: 4px;
    margin: 16px 0 8px 0;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="beam-banner">
  <div>
    <div style="font-family:'Orbitron',sans-serif;color:#00d4ff;font-size:1.5rem;
         letter-spacing:0.12em;font-weight:700">🏗 BEAM LAB</div>
    <p>2D Elastic Beam Analysis &nbsp;·&nbsp; Direct Stiffness Method &nbsp;·&nbsp; IS 800 Compatible</p>
  </div>
  <div style="margin-left:auto;display:flex;gap:8px;align-items:center">
    <span class="badge">v2.0</span>
    <span class="badge" style="background:#ffaa00">anaStruct</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PLOT THEME
# ─────────────────────────────────────────────────────────────────────────────
DARK_BG = "#080d18"
DARK_AX = "#0d1425"
CYAN    = "#00d4ff"
AMBER   = "#ffaa00"
RED_C   = "#ff4d6a"
GREEN_C = "#00e5a0"
TEXT_C  = "#c8ddf0"
GRID_C  = "#1e3a5f"

def style_ax(ax, title=""):
    ax.set_facecolor(DARK_AX)
    ax.tick_params(colors=TEXT_C, labelsize=8)
    ax.xaxis.label.set_color(TEXT_C)
    ax.yaxis.label.set_color(TEXT_C)
    ax.xaxis.label.set_fontfamily("monospace")
    ax.yaxis.label.set_fontfamily("monospace")
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_C)
    ax.grid(True, color=GRID_C, linewidth=0.5, linestyle="--", alpha=0.6)
    if title:
        ax.set_title(title, color=CYAN, fontsize=9.5,
                     fontfamily="monospace", pad=10)

def make_fig(h=3.8):
    fig, ax = plt.subplots(figsize=(11, h))
    fig.patch.set_facecolor(DARK_BG)
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
    with st.spinner("⚙ Solving system…"):
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

    # KPI strip
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("↕  R_left",   f"{R_lV:+.2f} kN")
    k2.metric("↕  R_right",  f"{R_rV:+.2f} kN")
    k3.metric("⟳  M_left",   f"{R_lM:+.2f} kN·m")
    k4.metric("⟳  M_right",  f"{R_rM:+.2f} kN·m")
    k5.metric("⬇  δ_max",    f"{max_def_mm:.3f} mm")

    st.markdown("<hr style='margin:10px 0 16px'>", unsafe_allow_html=True)

    # Collect diagram data
    x_pts, shear_vals, moment_vals, defl_vals = [], [], [], []
    for eid, el in ss.element_map.items():
        xi = el.vertex_1.x
        xj = el.vertex_2.x
        x_pts      += [xi, xj]
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

    # ── Tabs ─────────────────────────────────────────────────────────────────
    tab_sfd, tab_bmd, tab_def, tab_over, tab_data = st.tabs([
        "⚡  SHEAR FORCE",
        "🌀  BENDING MOMENT",
        "🔽  DEFLECTION",
        "🏗  STRUCTURE",
        "📋  REACTIONS",
    ])

    def annotate_peak(ax, xs, ys, color, unit):
        i = np.argmax(np.abs(ys))
        sign = 1 if ys[i] >= 0 else -1
        offset = sign * abs(ys[i]) * 0.45 + sign * (abs(ys).max() * 0.05)
        ax.annotate(
            f"{ys[i]:.2f} {unit}",
            xy=(xs[i], ys[i]),
            xytext=(xs[i], offset),
            color=color, fontsize=8.5, fontfamily="monospace",
            ha="center",
            arrowprops=dict(arrowstyle="-|>", color=color, lw=0.9),
        )

    # SFD
    with tab_sfd:
        fig, ax = make_fig()
        ax.fill_between(xs, Vs, 0, where=(Vs >= 0), color=CYAN,  alpha=0.22, interpolate=True)
        ax.fill_between(xs, Vs, 0, where=(Vs <  0), color=RED_C, alpha=0.22, interpolate=True)
        ax.plot(xs, Vs, color=CYAN, linewidth=2)
        ax.axhline(0, color=GRID_C, linewidth=0.8)
        ax.set_xlabel("x  (m)"); ax.set_ylabel("V  (kN)")
        style_ax(ax, "SHEAR FORCE DIAGRAM")
        annotate_peak(ax, xs, Vs, AMBER, "kN")
        fig.tight_layout(pad=1.5); st.pyplot(fig); plt.close(fig)

    # BMD
    with tab_bmd:
        fig, ax = make_fig()
        ax.fill_between(xs, Ms, 0, where=(Ms >= 0), color=AMBER,   alpha=0.22, interpolate=True)
        ax.fill_between(xs, Ms, 0, where=(Ms <  0), color=GREEN_C, alpha=0.22, interpolate=True)
        ax.plot(xs, Ms, color=AMBER, linewidth=2)
        ax.axhline(0, color=GRID_C, linewidth=0.8)
        ax.set_xlabel("x  (m)"); ax.set_ylabel("M  (kN·m)")
        style_ax(ax, "BENDING MOMENT DIAGRAM")
        annotate_peak(ax, xs, Ms, CYAN, "kN·m")
        fig.tight_layout(pad=1.5); st.pyplot(fig); plt.close(fig)

    # Deflection
    with tab_def:
        fig, ax = make_fig()
        ax.plot(xs, np.zeros_like(xs), color=GRID_C, lw=1.2,
                linestyle="--", label="Undeformed")
        ax.fill_between(xs, Ds, 0, color=GREEN_C, alpha=0.18, interpolate=True)
        ax.plot(xs, Ds, color=GREEN_C, linewidth=2, label="Deflected")
        ax.axhline(0, color=GRID_C, linewidth=0.6)
        ax.set_xlabel("x  (m)"); ax.set_ylabel("δ  (mm)")
        style_ax(ax, "DEFLECTED SHAPE")
        annotate_peak(ax, xs, Ds, AMBER, "mm")
        leg = ax.legend(fontsize=8, facecolor=DARK_AX, edgecolor=GRID_C)
        for t in leg.get_texts(): t.set_color(TEXT_C)
        fig.tight_layout(pad=1.5); st.pyplot(fig); plt.close(fig)

    # Structure
    with tab_over:
        fig, ax = make_fig(h=4.0)
        ax.plot([0, L], [0, 0], color=CYAN, linewidth=5,
                solid_capstyle="round", zorder=3)

        def draw_pinned(ax, x):
            tri = plt.Polygon([[x, 0], [x - 0.35, -0.45], [x + 0.35, -0.45]],
                               closed=True, color=AMBER, zorder=4, alpha=0.9)
            ax.add_patch(tri)
            ax.plot([x - 0.5, x + 0.5], [-0.52, -0.52], color=AMBER, lw=1.5)

        def draw_fixed(ax, x, side="left"):
            dx = -0.35 if side == "left" else 0.35
            for y in np.linspace(-0.5, 0.5, 7):
                ax.plot([x, x + dx], [y, y + dx * 0.6],
                        color=AMBER, lw=1.2, alpha=0.7)
            ax.plot([x, x], [-0.55, 0.55], color=AMBER, lw=2.5)

        def draw_roller(ax, x):
            c = plt.Circle((x, -0.28), 0.14, color=AMBER, zorder=4, alpha=0.9)
            ax.add_patch(c)
            ax.plot([x - 0.5, x + 0.5], [-0.45, -0.45], color=AMBER, lw=1.5)

        if left_support == "Pinned":              draw_pinned(ax, 0)
        elif left_support == "Fixed":             draw_fixed(ax, 0, "left")
        if right_support == "Pinned":             draw_pinned(ax, L)
        elif right_support == "Fixed":            draw_fixed(ax, L, "right")
        elif right_support == "Roller (vertical)":draw_roller(ax, L)

        # Point load
        if load_type in ("Point Load", "Both") and P != 0:
            d = -1 if P < 0 else 1
            ax.annotate("", xy=(x_load, 0), xytext=(x_load, d * 0.9),
                arrowprops=dict(arrowstyle="-|>", color=RED_C, lw=2.2,
                                mutation_scale=20))
            ax.text(x_load, d * 1.05, f"P = {P} kN", ha="center",
                    va="bottom" if d > 0 else "top",
                    color=RED_C, fontsize=9, fontfamily="monospace")

        # UDL
        if load_type in ("UDL", "Both") and q != 0:
            d = -1 if q < 0 else 1
            for xi in np.linspace(0.4, L - 0.4, 10):
                ax.annotate("", xy=(xi, 0), xytext=(xi, d * 0.65),
                    arrowprops=dict(arrowstyle="-|>", color=GREEN_C, lw=1.3,
                                    mutation_scale=13))
            ax.plot([0.4, L - 0.4], [d * 0.65, d * 0.65],
                    color=GREEN_C, lw=1.5, linestyle="--")
            ax.text(L / 2, d * 0.82, f"w = {q} kN/m", ha="center",
                    color=GREEN_C, fontsize=9, fontfamily="monospace")

        ax.set_xlim(-0.9, L + 0.9)
        ax.set_ylim(-1.1, 1.3)
        ax.set_xlabel("x  (m)")
        ax.set_yticks([])
        style_ax(ax, "LOADED STRUCTURE")
        fig.tight_layout(pad=1.5); st.pyplot(fig); plt.close(fig)

    # Reactions
    with tab_data:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Support Reactions")
            st.table({
                "Location":   ["Left",          "Right"],
                "V  (kN)":    [f"{R_lV:+.4f}",  f"{R_rV:+.4f}"],
                "H  (kN)":    [f"{R_lH:+.4f}",  "—"],
                "M  (kN·m)":  [f"{R_lM:+.4f}",  f"{R_rM:+.4f}"],
            })
        with c2:
            st.markdown("#### Configuration")
            st.table({
                "Parameter": ["L", "E", "I", "Left BC", "Right BC", "Load", "δ_max"],
                "Value":     [f"{L} m", f"{E_GPa} GPa", f"{I_cm4} cm⁴",
                              left_support, right_support, load_type,
                              f"{max_def_mm:.4f} mm"],
            })

        # Serviceability check
        if max_def_m > 0:
            ratio = L / max_def_m
            limit = 300
            ok    = ratio >= limit
            st.markdown(
                f"""<div style="margin-top:14px;padding:12px 20px;
                    background:#0d1425;border:1px solid #1e3a5f;border-radius:4px;
                    font-family:'Share Tech Mono',monospace;font-size:0.84rem;color:#c8ddf0">
                    {'✅' if ok else '❌'} &nbsp;
                    Serviceability check (IS 800 Cl. 5.6.1) &nbsp;|&nbsp;
                    <span style="color:#00d4ff">L / δ = {ratio:.0f}</span>
                    &nbsp;|&nbsp; Limit = L/{limit}
                    &nbsp;|&nbsp;
                    <span style="color:{'#00e5a0' if ok else '#ff4d6a'}">
                    {'PASS' if ok else 'FAIL'}</span>
                </div>""",
                unsafe_allow_html=True,
            )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:32px;padding:10px 0;border-top:1px solid #1e3a5f;
     font-family:'Share Tech Mono',monospace;font-size:0.68rem;color:#5a7a9a;
     display:flex;justify-content:space-between">
  <span>🏗 BEAM LAB &nbsp;·&nbsp; Direct Stiffness Method &nbsp;·&nbsp; anaStruct</span>
  <span>IS 800 : 2007 &nbsp;·&nbsp; IS 456 : 2000</span>
</div>
""", unsafe_allow_html=True)
