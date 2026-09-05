import streamlit as st

from style import apply_theme


st.set_page_config(
    page_title="Vehicle Analytics",
    page_icon="📊",
    layout="wide",
)

apply_theme()


# =========================================================
# HEADER
# =========================================================

st.title("📊 Vehicle Analytics Dashboard")

st.write(
    "Explore interactive analytics covering vehicle mileage, "
    "ethanol blends, driving conditions and vehicle performance."
)

st.caption(
    "📈 Mileage Trends  •  ⛽ Ethanol Analysis  •  🚗 Vehicle Performance"
)

st.divider()


# =========================================================
# ANALYTICS AREAS
# =========================================================

st.subheader("📈 Analytics Areas")

c1, c2, c3 = st.columns(3)

with c1:

    with st.container(border=True):

        st.markdown("### 📈 Mileage Trends")

        st.write(
            "Explore vehicle mileage patterns and identify "
            "important performance trends."
        )


with c2:

    with st.container(border=True):

        st.markdown("### ⛽ Ethanol Blend Analysis")

        st.write(
            "Study the relationship between ethanol blend "
            "and vehicle mileage."
        )


with c3:

    with st.container(border=True):

        st.markdown("### 🚗 Vehicle Performance")

        st.write(
            "Compare vehicle characteristics, driving conditions "
            "and mileage performance."
        )


st.divider()


# =========================================================
# TABLEAU
# =========================================================

st.subheader("📊 Interactive Tableau Dashboard")

st.write(
    "Open the dashboard below to explore the complete "
    "interactive business intelligence analysis."
)

st.link_button(
    "📊 Open Tableau Dashboard →",
    "https://public.tableau.com/app/profile/harsha.sharma2181/viz/ML_Project_17859431199460/Dashboard4",
    use_container_width=True,
)


st.divider()


# =========================================================
# INFORMATION
# =========================================================

c1, c2 = st.columns(2)

with c1:

    with st.container(border=True):

        st.markdown("### 🎯 Dashboard Purpose")

        st.write(
            "The dashboard helps analyze mileage behavior across "
            "different vehicles, ethanol blends and driving conditions."
        )


with c2:

    with st.container(border=True):

        st.markdown("### 💡 Key Questions")

        st.write(
            "• How does ethanol blend affect mileage?\n\n"
            "• Which vehicles perform better?\n\n"
            "• How do driving conditions influence mileage?"
        )


st.divider()

st.caption(
    "📊 Vehicle Mileage Analytics  |  Powered by Tableau"
)