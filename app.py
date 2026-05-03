import streamlit as st
from anastruct import SystemElements
import matplotlib.pyplot as plt

st.title("🏗️ Interactive Beam Lab")

# Sidebar - Geometry & Load
L = st.sidebar.slider("Beam Length (m)", 1, 20, 10)
P = st.sidebar.slider("Point Load (kN)", -100, 100, -50)
x_load = st.sidebar.slider("Load Position (m)", 0, L, L//2)

# Sidebar - Boundary Conditions
st.sidebar.subheader("Support Conditions")
left_support = st.sidebar.selectbox("Left Support", ["Pinned", "Fixed", "Roller"])
right_support = st.sidebar.selectbox("Right Support", ["Pinned", "Fixed", "Roller"])

# 1. Initialize System
ss = SystemElements()

# 2. Add Elements (Nodes at 0 and L)
ss.add_multiple_elements([[0, 0], [L, 0]])

# 3. Apply Supports (Indeterminate vs Determinate)
# Fixed: (spring_x, spring_y, spring_roll) = (0, 0, 0) means fully restrained
def apply_sup(node, type):
    if type == "Pinned":
        ss.add_support_hinged(node_id=node)
    elif type == "Fixed":
        ss.add_support_fixed(node_id=node)
    elif type == "Roller":
        ss.add_support_roll(node_id=node, direction=2)

apply_sup(1, left_support)
apply_sup(2, right_support)

# 4. Apply Load
ss.point_load(node_id=1, Fy=P) # Or use ss.q_load for UDL

# 5. Solve and Visualize
ss.solve()

# Display Results
fig_sfd = ss.show_shear_force(show=False)
st.subheader("Shear Force Diagram (SFD)")
st.pyplot(fig_sfd)

fig_bmd = ss.show_bending_moment(show=False)
st.subheader("Bending Moment Diagram (BMD)")
st.pyplot(fig_bmd)
