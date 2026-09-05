from pathlib import Path

import pandas as pd


# ==========================================================
# Project Paths
# ==========================================================

# Project root:
# D:/Vehicle_Mileage_Project
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset:
# D:/Vehicle_Mileage_Project/data/processed/cleaned_dataset.csv
CSV_PATH = BASE_DIR / "data" / "processed" / "cleaned_dataset.csv"


# ==========================================================
# Load Dataset
# ==========================================================

try:
    df = pd.read_csv(CSV_PATH)
    print("Dataset Loaded Successfully")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))

except FileNotFoundError:
    raise FileNotFoundError(
        f"Dataset not found at: {CSV_PATH}"
    )


# ==========================================================
# Search Vehicle
# ==========================================================

def search_vehicle(question: str) -> str:
    """
    Search the vehicle dataset using a user's question.

    The function looks for:
    1. Vehicle model
    2. Manufacturer

    Returns a text context containing vehicle statistics
    and sample records.
    """

    if not question or not question.strip():
        return ""

    question_lower = question.lower().strip()


    # ======================================================
    # Find Model
    # ======================================================

    model_matches = df[
        df["Model"]
        .astype(str)
        .str.lower()
        .apply(lambda x: x in question_lower)
    ]


    # ======================================================
    # Find Manufacturer
    # ======================================================

    manufacturer_matches = df[
        df["Manufacturer"]
        .astype(str)
        .str.lower()
        .apply(lambda x: x in question_lower)
    ]


    # ======================================================
    # Select Records
    # ======================================================

    if not model_matches.empty:
        results = model_matches

    elif not manufacturer_matches.empty:
        results = manufacturer_matches

    else:
        return ""


    # ======================================================
    # Vehicle Summary
    # ======================================================

    first_record = results.iloc[0]

    manufacturer = first_record["Manufacturer"]
    model = first_record["Model"]

    record_count = len(results)

    average_mileage = results["Mileage_km_per_L"].mean()
    minimum_mileage = results["Mileage_km_per_L"].min()
    maximum_mileage = results["Mileage_km_per_L"].max()


    context = f"""
VEHICLE DATASET SUMMARY

Vehicle: {manufacturer} {model}

Number of records found: {record_count}

Average Mileage: {average_mileage:.2f} km/L

Minimum Mileage: {minimum_mileage:.2f} km/L

Maximum Mileage: {maximum_mileage:.2f} km/L

The mileage values vary because the dataset contains
different vehicle and operating conditions.


SAMPLE VEHICLE RECORDS:
"""


    # ======================================================
    # Sample Records
    # ======================================================

    for _, row in results.head(10).iterrows():

        context += f"""
Manufacturer: {row['Manufacturer']}
Model: {row['Model']}
Vehicle Age: {row['Vehicle_Age']} years
Engine CC: {row['Engine_CC']} cc
Horsepower: {row['Horsepower']} HP
Vehicle Weight: {row['Vehicle_Weight']} kg
Transmission: {row['Transmission']}
Fuel Type: {row['Fuel_Type']}
Ethanol Blend: {row['Ethanol_Blend']}%
Average Speed: {row['Average_Speed']} km/h
Engine RPM: {row['Engine_RPM']}
Traffic Level: {row['Traffic_Level']}
Driving Style: {row['Driving_Style']}
AC Usage: {row['AC_Usage']}
Tire Pressure: {row['Tire_Pressure_PSI']} PSI
Road Type: {row['Road_Type']}
Weather: {row['Weather']}
Fuel Consumption: {row['Fuel_Consumption_L_100km']} L/100km
Mileage: {row['Mileage_km_per_L']} km/L
-----------------------------------------
"""


    return context