import streamlit as st
import pandas as pd
import joblib

# ======================================
# Page Configuration
# ======================================

st.set_page_config(
    page_title="Vehicle Mileage Prediction",
    page_icon="🚗",
    layout="wide"
)

# ======================================
# Load Model Files
# ======================================

best_model = joblib.load("models/best_model.pkl")
label_encoders = joblib.load("models/label_encoders.pkl")
feature_names = joblib.load("models/feature_names.pkl")

# ======================================
# Sidebar
# ======================================

st.sidebar.title("🚗 Vehicle Mileage Prediction")

st.sidebar.success("Model Loaded Successfully")

st.sidebar.markdown("---")

st.sidebar.subheader("📊 Model Information")

st.sidebar.write("**Algorithm:** CatBoost Regressor")
st.sidebar.write("**Hyperparameter Tuning:** GridSearchCV + RandomizedSearchCV")
st.sidebar.write("**Features Used:** 20")

st.sidebar.markdown("---")

st.sidebar.info(
    "This application predicts the mileage (km/L) of an ethanol blend vehicle."
)

# ======================================
# Main Title
# ======================================

st.title("🚗 Ethanol Blend Vehicle Mileage Prediction")

st.markdown("""
Enter the vehicle specifications and driving conditions below to predict the vehicle mileage.
""")

# ======================================
# Input Section
# ======================================

col1, col2 = st.columns(2)

# -----------------------------
# Left Column
# -----------------------------

with col1:

    st.subheader("🚘 Vehicle Details")

    vehicle_age = st.number_input(
        "Vehicle Age (Years)",
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
        "Vehicle Weight (kg)",
        min_value=500,
        max_value=3000,
        value=1100
    )

    transmission = st.selectbox(
        "Transmission",
        ["Automatic", "Manual"]
    )

    ethanol_blend = st.slider(
        "Ethanol Blend (%)",
        0,
        100,
        20
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

    engine_rpm = st.number_input(
        "Engine RPM",
        value=2400
    )

# -----------------------------
# Right Column
# -----------------------------

with col2:

    st.subheader("🌦 Driving Conditions")

    tire_pressure = st.number_input(
        "Tire Pressure (PSI)",
        value=32
    )

    maintenance = st.selectbox(
        "Maintenance Status",
        ["Good", "Average", "Poor"]
    )

    road = st.selectbox(
        "Road Type",
        ["City", "Highway", "Mixed", "Rural"]
    )

    traffic = st.selectbox(
        "Traffic Level",
        ["Low", "Medium", "High"]
    )

    temperature = st.number_input(
        "Temperature (°C)",
        value=30
    )

    humidity = st.number_input(
        "Humidity (%)",
        value=60
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

    passengers = st.slider(
        "Passengers",
        1,
        5,
        3
    )

# ======================================
# Prediction
# ======================================

if st.button("🚗 Predict Mileage", use_container_width=True):

    new_vehicle = pd.DataFrame({

        "Vehicle_Age":[vehicle_age],
        "Engine_CC":[engine_cc],
        "Horsepower":[horsepower],
        "Vehicle_Weight":[vehicle_weight],
        "Transmission":[transmission],
        "Ethanol_Blend":[ethanol_blend],
        "Fuel_Price":[fuel_price],
        "Trip_Distance_km":[trip_distance],
        "Average_Speed":[average_speed],
        "Engine_RPM":[engine_rpm],
        "Tire_Pressure_PSI":[tire_pressure],
        "Maintenance_Status":[maintenance],
        "Road_Type":[road],
        "Traffic_Level":[traffic],
        "Temperature":[temperature],
        "Humidity":[humidity],
        "Weather":[weather],
        "AC_Usage":[ac_usage],
        "Driving_Style":[driving],
        "Passengers":[passengers]

    })

    categorical_columns = [
        "Transmission",
        "Maintenance_Status",
        "Road_Type",
        "Traffic_Level",
        "Weather",
        "AC_Usage",
        "Driving_Style"
    ]

    # -----------------------------
    # Safe Encoding
    # -----------------------------

    try:

        for col in categorical_columns:
            new_vehicle[col] = label_encoders[col].transform(new_vehicle[col])

    except ValueError as e:

        st.error(f"Encoding Error: {e}")
        st.stop()

    # Arrange feature order

    new_vehicle = new_vehicle[feature_names]

    # -----------------------------
    # Prediction
    # -----------------------------

    with st.spinner("Predicting Vehicle Mileage..."):

        prediction = best_model.predict(new_vehicle)

    st.success("Prediction Completed Successfully ✅")

    # -----------------------------
    # Result
    # -----------------------------

    st.metric(
        label="🚗 Predicted Mileage",
        value=f"{prediction[0]:.2f} km/L"
    )

    # -----------------------------
    # Show Encoded Data
    # -----------------------------

    with st.expander("📋 Show Processed Input Data"):

        st.dataframe(new_vehicle)

# ======================================
# Footer
# ======================================

st.markdown("---")

st.caption(
    "Developed by Sujeet Badade | CDAC DBDA Final Project | Machine Learning using CatBoost Regressor"
)