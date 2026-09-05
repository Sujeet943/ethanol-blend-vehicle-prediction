import streamlit as st

from style import apply_theme


st.set_page_config(
    page_title="Ethanol Vehicle AI",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()


# =========================================================
# HERO
# =========================================================

st.title("🚗 Ethanol Vehicle AI Intelligence")

st.write(
    "An intelligent platform for vehicle mileage prediction, "
    "ethanol-blend analysis, GenAI assistance and interactive analytics."
)

st.caption(
    "⚡ Machine Learning   •   🤖 GenAI   •   🔎 RAG   •   📊 Business Intelligence"
)

st.divider()


# =========================================================
# PLATFORM MODULES
# =========================================================

st.subheader("🧭 Explore the Platform")

col1, col2, col3 = st.columns(3, gap="large")


with col1:

    with st.container(border=True):

        st.markdown("### 🧮 ML Mileage Predictor")

        st.write(
            "Predict vehicle mileage using the trained "
            "**CatBoost regression model**."
        )

        st.caption(
            "Enter vehicle and driving parameters to receive "
            "an instant mileage prediction."
        )

        if st.button(
            "Open Mileage Predictor →",
            key="predictor",
            use_container_width=True,
        ):
            st.switch_page("pages/1_ML_Prediction.py")


with col2:

    with st.container(border=True):

        st.markdown("### 🤖 GenAI Vehicle Assistant")

        st.write(
            "Ask questions about ethanol fuel, mileage, "
            "engine performance and vehicle behavior."
        )

        st.caption(
            "Hybrid RAG search + vehicle dataset + Groq LLM."
        )

        if st.button(
            "Open GenAI Assistant →",
            key="genai",
            use_container_width=True,
        ):
            st.switch_page("pages/2_GenAI_Assistant.py")


with col3:

    with st.container(border=True):

        st.markdown("### 📊 Vehicle Analytics")

        st.write(
            "Explore interactive vehicle mileage and "
            "ethanol-blend analytics."
        )

        st.caption(
            "Analyze trends and vehicle performance using Tableau."
        )

        if st.button(
            "Open Analytics Dashboard →",
            key="tableau",
            use_container_width=True,
        ):
            st.switch_page("pages/3_Tableau_Dashboard.py")


# =========================================================
# OVERVIEW
# =========================================================

st.divider()

st.subheader("📈 Platform Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("🚗 Vehicle Records", "63K+")

with c2:
    st.metric("📋 Features", "27")

with c3:
    st.metric("🔎 RAG Chunks", "763")

with c4:
    st.metric("🧩 Modules", "3")


# =========================================================
# TECHNOLOGY
# =========================================================

st.divider()

st.subheader("🛠 Technology Stack")

t1, t2, t3, t4, t5 = st.columns(5)

with t1:
    st.info("🧠 **Machine Learning**\n\nCatBoost")

with t2:
    st.success("🤖 **GenAI**\n\nGroq LLM")

with t3:
    st.info("🔎 **RAG**\n\nHybrid Search")

with t4:
    st.success("🗄 **Vector DB**\n\nChroma")

with t5:
    st.info("📊 **BI**\n\nTableau")


# =========================================================
# PROJECT INFORMATION
# =========================================================

st.divider()

with st.expander("ℹ️ About this project"):

    st.markdown(
        """
        ### 🎯 Project Goal

        Predict `Mileage_km_per_L` for vehicles operating under
        different ethanol-blend and driving conditions.

        ### 🧠 Machine Learning

        A trained **CatBoost regression model** is used for
        vehicle mileage prediction.

        ### 🤖 Generative AI

        The application combines **hybrid RAG retrieval**,
        vehicle dataset information and a Groq-hosted LLM.

        ### 📊 Business Intelligence

        Tableau provides interactive exploration of mileage,
        ethanol blend and vehicle performance.
        """
    )


st.divider()

st.caption(
    "🚗 Ethanol Vehicle AI Intelligence Platform  |  "
    "ML • RAG • GenAI • Business Intelligence"
)