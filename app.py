"""
Interactive Beam Lab — Improved Version
Fixes applied:
  • Correct node IDs: add_multiple_elements(n=10) creates nodes 1–11; right support = node 11
  • Load position mapped to nearest interior node index
  • show_shear_force / show_bending_moment syntax fixed (no hyperlinks)
  • Added UDL support, deflection diagram, reaction table, result metrics
  • Handled unstable-structure errors gracefully
  • Organised into tabs for a cleaner layout
"""

import streamlit as st
import matplotlib
matplotlib.use("Agg")          # non-interactive backend — must come before pyplot import
import matplotlib.pyplot as plt
import numpy as np
from anastruct import SystemElements

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Interactive Beam Lab",
    page_icon="🏗️",
    layout="wide",
)

st.title("🏗️ Interactive Beam Lab")
st.caption("Analyse simply-supported, fixed, propped-cantilever, and cantilever beams instantly.")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuration")

    # --- Geometry ---
    st.subheader("Geometry")
    L = st.slider("Beam Length (m)", 1, 20, 10)
    N_ELEM = 20                              # internal discretisation (fixed)

    # --- Material & Section ---
    st.subheader("Material & Section")
    E_GPa  = st.number_input("Young's Modulus E (GPa)", value=200.0, step=10.0, min_value=1.0)
    I_cm4  = st.number_input("Second Moment of Area I (cm⁴)", value=33000.0, step=500.0, min_value=1.0)
    E      = E_GPa  * 1e6   # kN/m²  (GPa → kN/m²)
    I      = I_cm4  * 1e-8  # m⁴     (cm⁴ → m⁴)
    EA     = E * 1e-2        # axial stiffness placeholder (not critical for beams)

    # --- Loads ---
    st.subheader("Loads")
    load_type = st.radio("Load Type", ["Point Load", "UDL", "Both"])

    P, x_load = 0.0, L / 2
    q         = 0.0

    if load_type in ("Point Load", "Both"):
        P      = st.slider("Point Load (kN)  [−ve = downward]", -200, 200, -50)
        x_load = st.slider("Load Position (m)", 0.0, float(L), float(L) / 2, step=0.5)

    if load_type in ("UDL", "Both"):
        q = st.slider("UDL Intensity (kN/m)  [−ve = downward]", -50, 50, -10)

    # --- Supports ---
    st.subheader("Support Conditions")
    left_support  = st.selectbox("Left Support",  ["Pinned", "Fixed", "Free"])
    right_support = st.selectbox("Right Support", ["Pinned", "Fixed", "Roller (vertical)"])

# ── Helper: apply support ────────────────────────────────────────────────────
def apply_support(ss: SystemElements, node_id: int, support_type: str):
    if support_type == "Pinned":
        ss.add_support_hinged(node_id=node_id)
    elif support_type == "Fixed":
        ss.add_support_fixed(node_id=node_id)
    elif support_type == "Roller (vertical)":
        ss.add_support_roll(node_id=node_id, direction=2)
    # "Free" → no support added (cantilever tip, etc.)


# ── Build & solve ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def run_analysis(L, E, I, EA, P, x_load, q, left_support, right_support, N_ELEM, load_type):
    ss = SystemElements(EI=E * I, EA=EA)

    # Nodes 1 … N_ELEM+1  (left = 1, right = N_ELEM+1)
    ss.add_multiple_elements([[0, 0], [L, 0]], n=N_ELEM)

    node_left  = 1
    node_right = N_ELEM + 1

    apply_support(ss, node_left,  left_support)
    apply_support(ss, node_right, right_support)

    # --- Point load: snap to nearest node ---
    if load_type in ("Point Load", "Both") and P != 0:
        frac      = np.clip(x_load / L, 0, 1)
        load_node = max(1, min(N_ELEM + 1, round(frac * N_ELEM) + 1))
        ss.point_load(node_id=load_node, Fy=P)

    # --- UDL: applied to all elements ---
    if load_type in ("UDL", "Both") and q != 0:
        for eid in range(1, N_ELEM + 1):
            ss.q_load(q=q, element_id=eid)

    ss.solve()
    return ss

try:
    with st.spinner("Solving…"):
        ss = run_analysis(L, E, I, EA, P, x_load, q, left_support, right_support, N_ELEM, load_type)
    solved = True
except Exception as exc:
    solved = False
    st.error(f"⚠️ Analysis failed — check boundary conditions. Detail: {exc}")


# ── Results ───────────────────────────────────────────────────────────────────
if solved:
    # --- Collect numerical results ---
    disp  = ss.get_node_displacements()
    react = ss.get_support_reaction_forces()

    # Max vertical displacement
    max_def_mm = max(abs(v["Fy"]) * 1e3 for v in disp.values()) if disp else 0.0

    # Collect reactions for left & right nodes
    node_left_id  = 1
    node_right_id = N_ELEM + 1

    def get_reaction(node_id, component):
        r = react.get(node_id, {})
        return r.get(component, 0.0)

    R_left_V  = get_reaction(node_left_id,  "Fy")
    R_right_V = get_reaction(node_right_id, "Fy")
    R_left_H  = get_reaction(node_left_id,  "Fx")
    R_left_M  = get_reaction(node_left_id,  "Mz")
    R_right_M = get_reaction(node_right_id, "Mz")

    # ── Metrics row ───────────────────────────────────────────────────────────
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("↕ Left Reaction",   f"{R_left_V:.2f} kN")
    c2.metric("↕ Right Reaction",  f"{R_right_V:.2f} kN")
    c3.metric("⟳ Left Moment",     f"{R_left_M:.2f} kN·m")
    c4.metric("⬇ Max Deflection",  f"{max_def_mm:.3f} mm")

    # ── Tabs ─────────────────────────────────────────────────────────────────
    tab_sfd, tab_bmd, tab_def, tab_struct, tab_info = st.tabs([
        "📊 Shear Force", "📈 Bending Moment", "🔽 Deflection",
        "🏗️ Structure", "📋 Reactions"
    ])

    def tight_fig(fig):
        """Apply consistent styling to anastruct figures."""
        fig.set_size_inches(10, 3.5)
        fig.tight_layout()
        return fig

    with tab_sfd:
        st.subheader("Shear Force Diagram")
        fig_sfd = ss.show_shear_force(show=False)
        st.pyplot(tight_fig(fig_sfd))
        plt.close(fig_sfd)

    with tab_bmd:
        st.subheader("Bending Moment Diagram")
        fig_bmd = ss.show_bending_moment(show=False)
        st.pyplot(tight_fig(fig_bmd))
        plt.close(fig_bmd)

    with tab_def:
        st.subheader("Deflected Shape")
        fig_def = ss.show_displacement(show=False)
        st.pyplot(tight_fig(fig_def))
        plt.close(fig_def)

    with tab_struct:
        st.subheader("Loaded Structure")
        fig_str = ss.show_structure(show=False)
        st.pyplot(tight_fig(fig_str))
        plt.close(fig_str)

    with tab_info:
        st.subheader("Support Reaction Summary")

        data = {
            "Support":          ["Left",        "Right"],
            "Vertical (kN)":    [f"{R_left_V:.3f}",  f"{R_right_V:.3f}"],
            "Horizontal (kN)":  [f"{R_left_H:.3f}",  "—"],
            "Moment (kN·m)":    [f"{R_left_M:.3f}",  f"{R_right_M:.3f}"],
        }
        st.table(data)

        st.subheader("Configuration Summary")
        st.markdown(f"""
| Parameter | Value |
|---|---|
| Beam length | {L} m |
| Young's modulus | {E_GPa} GPa |
| Second moment of area | {I_cm4} cm⁴ |
| Left support | {left_support} |
| Right support | {right_support} |
| Load type | {load_type} |
| Point load | {P} kN @ {x_load} m |
| UDL | {q} kN/m |
        """)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Built with [anaStruct](https://github.com/ritchie46/anaStruct) · Structural analysis engine")
