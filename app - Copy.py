"""Main Landing Page — Interactive navigation hub."""
import streamlit as st

st.set_page_config(
    page_title="Ethanol Mileage AI | Home",
    page_icon="🚀",
    layout="wide",
)

# ---------- Header ----------
st.markdown(
    """
    <style>
        .big-btn button {
            height: 110px;
            font-size: 1.15rem;
            font-weight: 700;
            border-radius: 14px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🚀 AI-Powered Ethanol Vehicle Mileage Prediction")
st.markdown(
    "Select a module below to explore the project. "
    "Each section is fully interactive — your inputs drive real-time ML inference, "
    "GenAI insights, and BI dashboards."
)
st.divider()

# ---------- Navigation Buttons ----------
st.subheader("🧭 Choose a Module")

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("##### 🧮 ML Mileage Predictor")
    st.caption("Input vehicle parameters and get an instant XGBoost mileage prediction.")
    if st.button("Open ML Predictor", key="btn_predictor", use_container_width=True):
        st.switch_page("pages/1_ML_Prediction.py")

with col2:
    st.markdown("##### 🤖 GenAI Insights & Summary")
    st.caption("RAG + Grok (xAI) generate grounded, fact-based recommendations.")
    if st.button("Open GenAI Insights", key="btn_genai", use_container_width=True):
        st.switch_page("pages/2_GenAI_Assistant.py")

with col3:
    st.markdown("##### 📈 Tableau Dashboard")
    st.caption("Interactive EDA dashboard embedded from Tableau Public.")
    if st.button("Open Tableau Dashboard", key="btn_tableau", use_container_width=True):
        st.switch_page("pages/3_Tableau_Dashboard.py")

st.divider()

# ---------- Quick Project Snapshot ----------
with st.expander("ℹ️ About this project", expanded=False):
    st.markdown(
        """
        - **Goal**: Predict `Mileage_km_per_L` for ethanol-blend fuel vehicles.
        - **ML**: catboost regressor (R² ≈ 0.9).
        - **GenAI**: LangChain + Grok LLM for grounded insights.
        - **BI**: Embedded Tableau Public dashboard for EDA.
        """
    )