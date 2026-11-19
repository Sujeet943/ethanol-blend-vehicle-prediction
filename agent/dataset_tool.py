import pandas as pd


# ==========================================================
# Load Dataset
# ==========================================================

CSV_PATH = r"D:\Vehicle_Mileage_Project\data\processed\cleaned_dataset.csv"

df = pd.read_csv(CSV_PATH)

print("Dataset Loaded Successfully")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# ==========================================================
# Dataset Search
# ==========================================================

def dataset_tool(question):
    """
    Answers vehicle dataset related questions.

    Examples:
    - What is the average mileage of Honda City?
    - What is the minimum mileage of Honda City?
    - What is the maximum mileage of Honda City?
    """

    question_lower = question.lower()

    # ------------------------------------------------------
    # Detect Manufacturer / Model
    # ------------------------------------------------------

    manufacturer = None
    model = None

    if "honda city" in question_lower:
        manufacturer = "Honda"
        model = "City"

    elif "honda" in question_lower:
        manufacturer = "Honda"

    # ------------------------------------------------------
    # Filter Dataset
    # ------------------------------------------------------

    filtered_df = df.copy()

    if manufacturer:

        filtered_df = filtered_df[
            filtered_df["Manufacturer"].str.lower()
            == manufacturer.lower()
        ]

    if model:

        filtered_df = filtered_df[
            filtered_df["Model"].str.lower()
            == model.lower()
        ]

    # ------------------------------------------------------
    # No Data
    # ------------------------------------------------------

    if filtered_df.empty:

        return "No matching vehicle records found in the dataset."

    # ------------------------------------------------------
    # Average Mileage
    # ------------------------------------------------------

    if "average mileage" in question_lower:

        avg_mileage = filtered_df[
            "Mileage_km_per_L"
        ].mean()

        return f"""
Vehicle Dataset Summary

Vehicle: {manufacturer} {model}

Number of records: {len(filtered_df)}

Average Mileage: {avg_mileage:.2f} km/L
"""

    # ------------------------------------------------------
    # Minimum Mileage
    # ------------------------------------------------------

    elif "minimum mileage" in question_lower \
            or "min mileage" in question_lower:

        min_mileage = filtered_df[
            "Mileage_km_per_L"
        ].min()

        return f"""
Vehicle Dataset Summary

Vehicle: {manufacturer} {model}

Minimum Mileage: {min_mileage:.2f} km/L
"""

    # ------------------------------------------------------
    # Maximum Mileage
    # ------------------------------------------------------

    elif "maximum mileage" in question_lower \
            or "max mileage" in question_lower:

        max_mileage = filtered_df[
            "Mileage_km_per_L"
        ].max()

        return f"""
Vehicle Dataset Summary

Vehicle: {manufacturer} {model}

Maximum Mileage: {max_mileage:.2f} km/L
"""

    # ------------------------------------------------------
    # Default
    # ------------------------------------------------------

    else:

        avg_mileage = filtered_df[
            "Mileage_km_per_L"
        ].mean()

        min_mileage = filtered_df[
            "Mileage_km_per_L"
        ].min()

        max_mileage = filtered_df[
            "Mileage_km_per_L"
        ].max()

        return f"""
Vehicle Dataset Summary

Vehicle: {manufacturer} {model}

Number of records: {len(filtered_df)}

Average Mileage: {avg_mileage:.2f} km/L

Minimum Mileage: {min_mileage:.2f} km/L

Maximum Mileage: {max_mileage:.2f} km/L
"""