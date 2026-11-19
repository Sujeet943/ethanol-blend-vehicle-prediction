import joblib
import pandas as pd

# ==========================
# Load Model
# ==========================

best_model = joblib.load("models/best_model.pkl")
label_encoders = joblib.load("models/label_encoders.pkl")
feature_names = joblib.load("models/feature_names.pkl")


def predict_mileage(vehicle_data):

    # Convert dictionary to DataFrame
    df = pd.DataFrame([vehicle_data])

    # ==========================
    # Encode categorical columns
    # ==========================

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

        if col in df.columns:
            df[col] = label_encoders[col].transform(df[col])

    # ==========================
    # Keep only model features
    # ==========================

    df = df[feature_names]

    # ==========================
    # Debug (Temporary)
    # ==========================

    print("=" * 60)
    print("Input sent to CatBoost")
    print("=" * 60)
    print(df)
    print()
    print(df.dtypes)
    print("=" * 60)

    # ==========================
    # Predict
    # ==========================

    prediction = best_model.predict(df)

    return round(float(prediction[0]), 2)