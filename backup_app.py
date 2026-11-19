from rag.rag_chain import ask_rag
from genai.helper import mileage_explanation
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
# Load Model
# ======================================

@st.cache_resource
def load_files():
    model = joblib.load("models/best_model.pkl")
    encoders = joblib.load("models/label_encoders.pkl")
    features = joblib.load("models/feature_names.pkl")
    return model, encoders, features

best_model, label_encoders, feature_names = load_files()

# ======================================
# Sidebar
# ======================================

st.sidebar.title("🚗 Vehicle Mileage Prediction")

st.sidebar.success("Model Loaded Successfully")

st.sidebar.markdown("---")

st.sidebar.subheader("📊 Model Information")
st.sidebar.write("Algorithm: CatBoost Regressor")
st.sidebar.write("Hyperparameter Tuning: GridSearchCV + RandomizedSearchCV")
st.sidebar.write("Features Used: 20")

st.sidebar.markdown("---")

st.sidebar.info(
    "Predict mileage of ethanol blend vehicles using Machine Learning."
)

# ======================================
# Main Title
# ======================================

st.title("🚗 Ethanol Blend Vehicle Mileage Prediction")

st.write(
    "Enter vehicle specifications and driving conditions to predict mileage."
)

# ======================================
# Input Layout
# ======================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("🚘 Vehicle Details")

    vehicle_age = st.number_input("Vehicle Age",0,20,5)

    engine_cc = st.number_input("Engine CC",800,3000,1200)

    horsepower = st.number_input("Horsepower",40,300,95)

    vehicle_weight = st.number_input("Vehicle Weight (kg)",500,3000,1100)

    transmission = st.selectbox(
        "Transmission",
        ["Automatic","Manual"]
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
        "Average Speed",
        value=65.0
    )

    engine_rpm = st.number_input(
        "Engine RPM",
        value=2400
    )

with col2:

    st.subheader("🌦 Driving Conditions")

    tire_pressure = st.number_input(
        "Tire Pressure (PSI)",
        value=32
    )

    maintenance = st.selectbox(
        "Maintenance Status",
        ["Good","Average","Poor"]
    )

    road = st.selectbox(
        "Road Type",
        ["City","Highway","Mixed","Rural"]
    )

    traffic = st.selectbox(
        "Traffic Level",
        ["Low","Medium","High"]
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
        ["Clear","Fog","Rain"]
    )

    ac_usage = st.selectbox(
        "AC Usage",
        ["Yes","No"]
    )

    driving = st.selectbox(
        "Driving Style",
        ["Smooth","Normal","Aggressive"]
    )

    passengers = st.slider(
        "Passengers",
        1,
        5,
        3
    )

# ======================================
# Predict Button
# ======================================

st.markdown("---")

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

    for col in categorical_columns:
        new_vehicle[col] = label_encoders[col].transform(new_vehicle[col])

    new_vehicle = new_vehicle[feature_names]

    prediction = best_model.predict(new_vehicle)

    predicted_mileage = round(float(prediction[0]),2)

    vehicle_data = {

        "Vehicle Age":vehicle_age,
        "Engine CC":engine_cc,
        "Horsepower":horsepower,
        "Vehicle Weight":vehicle_weight,
        "Transmission":transmission,
        "Ethanol Blend (%)":ethanol_blend,
        "Fuel Price":fuel_price,
        "Trip Distance":trip_distance,
        "Average Speed":average_speed,
        "Engine RPM":engine_rpm,
        "Tire Pressure":tire_pressure,
        "Maintenance":maintenance,
        "Road Type":road,
        "Traffic":traffic,
        "Temperature":temperature,
        "Humidity":humidity,
        "Weather":weather,
        "AC Usage":ac_usage,
        "Driving Style":driving,
        "Passengers":passengers

    }

    st.session_state["vehicle_data"] = vehicle_data
    st.session_state["prediction"] = predicted_mileage
    st.session_state["processed"] = new_vehicle

# ======================================
# Prediction Result
# ======================================

if "prediction" in st.session_state:

    st.success("Prediction Completed Successfully")

    st.metric(
        "🚗 Predicted Mileage",
        f"{st.session_state['prediction']} km/L"
    )

    if st.button("🤖 Generate AI Analysis", use_container_width=True):

        with st.spinner("Generating AI explanation..."):

            explanation = mileage_explanation(
                st.session_state["vehicle_data"],
                st.session_state["prediction"]
            )

        st.markdown("---")

        st.markdown(explanation)

    with st.expander("📋 Show Processed Input Data"):

        st.dataframe(st.session_state["processed"])

# ======================================
# Footer
# ======================================

st.markdown("---")

st.caption(
    "Developed by Sujeet Badade | CDAC DBDA Final Project | Machine Learning using CatBoost Regressor"
)
# ======================================
# RAG Chatbot
# ======================================

st.markdown("---")
st.header("📚 Vehicle Knowledge Assistant (RAG)")

user_question = st.text_input(
    "Ask anything about ethanol blend vehicles:"
)

if st.button("Ask Question"):

    if user_question.strip() == "":
        st.warning("Please enter a question.")
    else:

        with st.spinner("Searching documents..."):

            answer = ask_rag(user_question)

        st.success("Answer")

        st.write(answer)