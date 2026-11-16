
import streamlit as st
import pandas as pd
import joblib

from genai.helper import mileage_explanation


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Vehicle Mileage Prediction",
    page_icon="🚗",
    layout="wide"
)


# ==========================================================
# DIRECT PAGE STYLING
# ==========================================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #e8f7ff 0%,
            #f4fff9 50%,
            #e9f8f5 100%
        ) !important;
    }

    .main {
        background: transparent !important;
    }

    .block-container {
        max-width: 1200px !important;
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #e3f5fc 0%,
            #eafbf5 100%
        ) !important;

        border-right: 1px solid #c5e2e8 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #07527a !important;
    }

    h1 {
        color: #07527a !important;
        font-weight: 800 !important;
    }

    h2 {
        color: #086080 !important;
        font-weight: 750 !important;
    }

    h3 {
        color: #08705f !important;
        font-weight: 700 !important;
    }

    p {
        color: #285b72 !important;
    }

    label {
        color: #145873 !important;
        font-weight: 600 !important;
    }

    [data-testid="stWidgetLabel"] {
        color: #145873 !important;
    }

    [data-testid="stWidgetLabel"] p {
        color: #145873 !important;
    }

    div[data-testid="stNumberInput"] div[data-baseweb="input"] {
        background-color: #dff2f8 !important;
        border: 1px solid #b6dce7 !important;
        border-radius: 9px !important;
    }

    div[data-testid="stNumberInput"] div[data-baseweb="input"] > div {
        background-color: #dff2f8 !important;
        border: none !important;
    }

    div[data-testid="stNumberInput"] input {
        background-color: #dff2f8 !important;
        color: #164f68 !important;
        -webkit-text-fill-color: #164f68 !important;
    }

    div[data-testid="stNumberInput"] button {
        background-color: #dff2f8 !important;
        color: #07527a !important;
        border: none !important;
    }

    div[data-testid="stNumberInput"] button:hover {
        background-color: #cceaf3 !important;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background-color: #dff5ed !important;
        border: 1px solid #b7ded1 !important;
        border-radius: 9px !important;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #dff5ed !important;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] * {
        color: #145873 !important;
    }

    div[data-testid="stSelectbox"] svg {
        fill: #08705f !important;
    }

    div[data-testid="stSlider"] [data-baseweb="slider"] {
        margin-top: 5px;
    }

    div[data-testid="stSlider"] [role="slider"] {
        background-color: #42a889 !important;
        border: 2px solid #42a889 !important;
    }

    div[data-testid="stSlider"] div[data-testid="stTickBar"] {
        background-color: #d0e8df !important;
    }

    div.stButton > button {
        background: linear-gradient(
            90deg,
            #d7eef8,
            #d9f3e8
        ) !important;

        color: #07527a !important;
        border: 1px solid #a9d5df !important;
        border-radius: 9px !important;
        min-height: 45px !important;
        font-weight: 700 !important;

        box-shadow: 0 2px 6px rgba(
            30,
            100,
            120,
            0.08
        ) !important;
    }

    div.stButton > button p {
        color: #07527a !important;
        font-weight: 700 !important;
    }

    div.stButton > button:hover {
        background: linear-gradient(
            90deg,
            #c7e9f5,
            #c8eddf
        ) !important;

        border-color: #7fc2d0 !important;
        color: #064b6d !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(
            255,
            255,
            255,
            0.42
        ) !important;

        border: 1px solid #c7e3e3 !important;
        border-radius: 12px !important;

        box-shadow: 0 2px 8px rgba(
            30,
            100,
            120,
            0.04
        ) !important;
    }

    div[data-testid="stAlert"] {
        border-radius: 9px !important;
    }

    [data-testid="stMetric"] {
        background: linear-gradient(
            135deg,
            #e1f4fb,
            #e0f6ed
        ) !important;

        border: 1px solid #c2e0e1 !important;
        border-radius: 12px !important;
        padding: 18px !important;
    }

    [data-testid="stMetricLabel"] {
        color: #377083 !important;
    }

    [data-testid="stMetricValue"] {
        color: #07527a !important;
        font-weight: 800 !important;
    }

    div[data-testid="stExpander"] {
        background-color: #eefaf7 !important;
        border: 1px solid #c5e1dc !important;
        border-radius: 10px !important;
    }

    div[data-testid="stExpander"] summary {
        color: #07527a !important;
    }

    div[data-testid="stExpander"] summary p {
        color: #07527a !important;
        font-weight: 600 !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #c5e1e3 !important;
        border-radius: 8px !important;
    }

    hr {
        border-color: #c5e0e3 !important;
    }

    .stMarkdown {
        color: #285b72 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# LOAD ML MODEL FILES
# ==========================================================

@st.cache_resource
def load_files():

    model = joblib.load("models/best_model.pkl")

    encoders = joblib.load(
        "models/label_encoders.pkl"
    )

    features = joblib.load(
        "models/feature_names.pkl"
    )

    return model, encoders, features


best_model, label_encoders, feature_names = load_files()


# ==========================================================
# PAGE TITLE
# ==========================================================

st.title("🚗 Vehicle Mileage Prediction")

st.write(
    "Predict vehicle mileage using the trained CatBoost model."
)


# ==========================================================
# HIDDEN INPUTS - DEFAULT VALUES
# ==========================================================

# These seven inputs are hidden from the user interface.
# They are still passed internally to the trained model.

transmission = "Automatic"

engine_rpm = 2400

tire_pressure = 32.0

road = "City"

temperature = 30.0

humidity = 60.0

passengers = 3


# ==========================================================
# INPUT SECTION
# ==========================================================

col1, col2 = st.columns(2, gap="large")


# ==========================================================
# VEHICLE INFORMATION
# ==========================================================

with col1:

    st.subheader("Vehicle Information")

    vehicle_age = st.number_input(
        "Vehicle Age",
        min_value=0,
        max_value=20,
        value=5
    )

    engine_cc = st.number_input(
        "Engine CC",
        min_value=800,
        max_value=3000,
        value=1200
    )

    horsepower = st.number_input(
        "Horsepower",
        min_value=40,
        max_value=300,
        value=95
    )

    vehicle_weight = st.number_input(
        "Vehicle Weight",
        min_value=500,
        max_value=3000,
        value=1100
    )

    ethanol_blend = st.slider(
        "Ethanol Blend (%)",
        min_value=0,
        max_value=100,
        value=20
    )

    fuel_price = st.number_input(
        "Fuel Price",
        value=104.0
    )

    trip_distance = st.number_input(
        "Trip Distance (km)",
        value=150.0
    )

    average_speed = st.number_input(
        "Average Speed (km/h)",
        value=65.0
    )


# ==========================================================
# DRIVING INFORMATION
# ==========================================================

with col2:

    st.subheader("Driving Information")

    maintenance = st.selectbox(
        "Maintenance Status",
        ["Good", "Average", "Poor"]
    )

    traffic = st.selectbox(
        "Traffic Level",
        ["Low", "Medium", "High"]
    )

    weather = st.selectbox(
        "Weather",
        ["Clear", "Fog", "Rain"]
    )

    ac_usage = st.selectbox(
        "AC Usage",
        ["Yes", "No"]
    )

    driving = st.selectbox(
        "Driving Style",
        ["Smooth", "Normal", "Aggressive"]
    )


# ==========================================================
# PREDICTION BUTTON
# ==========================================================

st.divider()

if st.button(
    "🔮 Predict Mileage",
    use_container_width=True
):

    # ------------------------------------------------------
    # CREATE COMPLETE INPUT DATAFRAME FOR MODEL
    # ------------------------------------------------------

    new_vehicle = pd.DataFrame({

        "Vehicle_Age": [vehicle_age],

        "Engine_CC": [engine_cc],

        "Horsepower": [horsepower],

        "Vehicle_Weight": [vehicle_weight],

        "Transmission": [transmission],

        "Ethanol_Blend": [ethanol_blend],

        "Fuel_Price": [fuel_price],

        "Trip_Distance_km": [trip_distance],

        "Average_Speed": [average_speed],

        "Engine_RPM": [engine_rpm],

        "Tire_Pressure_PSI": [tire_pressure],

        "Maintenance_Status": [maintenance],

        "Road_Type": [road],

        "Traffic_Level": [traffic],

        "Temperature": [temperature],

        "Humidity": [humidity],

        "Weather": [weather],

        "AC_Usage": [ac_usage],

        "Driving_Style": [driving],

        "Passengers": [passengers]
    })


    # ------------------------------------------------------
    # ENCODE CATEGORICAL VARIABLES
    # ------------------------------------------------------

    categorical_columns = [

        "Transmission",

        "Maintenance_Status",

        "Road_Type",

        "Traffic_Level",

        "Weather",

        "AC_Usage",

        "Driving_Style"
    ]


    for col in categorical_columns:

        new_vehicle[col] = (
            label_encoders[col]
            .transform(new_vehicle[col])
        )


    # ------------------------------------------------------
    # ARRANGE FEATURES AS EXPECTED BY MODEL
    # ------------------------------------------------------

    new_vehicle = new_vehicle[
        feature_names
    ]


    # ------------------------------------------------------
    # PREDICTION
    # ------------------------------------------------------

    prediction = best_model.predict(
        new_vehicle
    )

    predicted_mileage = round(
        float(prediction[0]),
        2
    )


    # ------------------------------------------------------
    # SAVE RESULTS
    # ------------------------------------------------------

    vehicle_data = {

        "Vehicle Age": vehicle_age,

        "Engine CC": engine_cc,

        "Horsepower": horsepower,

        "Vehicle Weight": vehicle_weight,

        "Transmission": transmission,

        "Ethanol Blend (%)": ethanol_blend,

        "Fuel Price": fuel_price,

        "Trip Distance": trip_distance,

        "Average Speed": average_speed,

        "Engine RPM": engine_rpm,

        "Tyre Pressure": tire_pressure,

        "Maintenance": maintenance,

        "Road Type": road,

        "Traffic": traffic,

        "Temperature": temperature,

        "Humidity": humidity,

        "Weather": weather,

        "AC Usage": ac_usage,

        "Driving Style": driving,

        "Passengers": passengers
    }


    st.session_state.predicted_mileage = (
        predicted_mileage
    )

    st.session_state.vehicle_data = (
        vehicle_data
    )

    # Keep all original features for model compatibility
    st.session_state.processed_input = (
        new_vehicle.copy()
    )


# ==========================================================
# DISPLAY PREDICTION
# ==========================================================

if "predicted_mileage" in st.session_state:

    st.divider()

    st.subheader("📊 Prediction Result")

    st.success(
        "Prediction Completed"
    )

    st.metric(
        "Predicted Mileage",
        f"{st.session_state.predicted_mileage} km/L"
    )


    # ======================================================
    # AI EXPLANATION
    # ======================================================

    st.subheader("🤖 AI Explanation")

    if st.button(
        "Generate AI Explanation",
        use_container_width=True
    ):

        with st.spinner(
            "Generating AI explanation..."
        ):

            try:

                explanation = mileage_explanation(
                    st.session_state.vehicle_data,
                    st.session_state.predicted_mileage
                )

                st.markdown(
                    explanation
                )

            except Exception as e:

                st.error(
                    f"AI explanation failed: {e}"
                )


    # ======================================================
    # PROCESSED INPUT - HIDE 7 FEATURES
    # ======================================================

    with st.expander(
        "🔍 View Processed Input"
    ):

        if "processed_input" in st.session_state:

            hidden_features = [

                "Transmission",

                "Engine_RPM",

                "Tire_Pressure_PSI",

                "Road_Type",

                "Temperature",

                "Humidity",

                "Passengers"
            ]

            display_input = (
                st.session_state.processed_input
                .drop(
                    columns=hidden_features,
                    errors="ignore"
                )
            )

            st.dataframe(
                display_input,
                use_container_width=True
            )

        else:

            st.info(
                "Generate a prediction first."
            )
