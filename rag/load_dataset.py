import pandas as pd

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

# ======================================
# Load Dataset
# ======================================

csv_path = r"D:\Vehicle_Mileage_Project\data\processed\cleaned_dataset.csv"

df = pd.read_csv(csv_path)

print("=" * 60)
print("Dataset Loaded Successfully")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("=" * 60)

# ======================================
# Convert Dataset into Documents
# ======================================

documents = []

for index, row in df.iterrows():

    text = f"""
Vehicle ID: {row['Vehicle_ID']}
Manufacturer: {row['Manufacturer']}
Model: {row['Model']}

Vehicle Age: {row['Vehicle_Age']} years
Engine CC: {row['Engine_CC']} cc
Horsepower: {row['Horsepower']} HP
Vehicle Weight: {row['Vehicle_Weight']} kg

Transmission: {row['Transmission']}
Fuel Type: {row['Fuel_Type']}
Ethanol Blend: {row['Ethanol_Blend']}

Fuel Price: {row['Fuel_Price']}

Trip Distance: {row['Trip_Distance_km']} km
Average Speed: {row['Average_Speed']} km/h
Engine RPM: {row['Engine_RPM']}

Tyre Pressure: {row['Tire_Pressure_PSI']} PSI
Maintenance Status: {row['Maintenance_Status']}

Road Type: {row['Road_Type']}
Traffic Level: {row['Traffic_Level']}

Temperature: {row['Temperature']} °C
Humidity: {row['Humidity']} %

Weather: {row['Weather']}
AC Usage: {row['AC_Usage']}
Driving Style: {row['Driving_Style']}
Passengers: {row['Passengers']}

CO2 Emission: {row['CO2_Emission_g_km']} g/km
Fuel Consumption: {row['Fuel_Consumption_L_100km']} L/100km

Mileage: {row['Mileage_km_per_L']} km/L
"""

    documents.append(
        Document(
            page_content=text,
            metadata={
                "row_id": int(index),
                "manufacturer": str(row["Manufacturer"]),
                "model": str(row["Model"]),
                "transmission": str(row["Transmission"]),
                "fuel_type": str(row["Fuel_Type"]),
                "ethanol_blend": str(row["Ethanol_Blend"]),
                "road_type": str(row["Road_Type"]),
                "traffic_level": str(row["Traffic_Level"]),
                "driving_style": str(row["Driving_Style"]),
                "weather": str(row["Weather"]),
                "maintenance": str(row["Maintenance_Status"]),
                "mileage": float(row["Mileage_km_per_L"])
            }
        )
    )

print("Documents Created:", len(documents))

# ======================================
# Embedding Model
# ======================================

print("\nLoading Embedding Model...")

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

print("Embedding Model Loaded.")

# ======================================
# Create ChromaDB
# ======================================

print("\nCreating Chroma Database...")

vectordb = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    collection_name="vehicle_dataset",
    persist_directory="chroma_dataset"
)

print("\n" + "=" * 60)
print("Dataset Stored Successfully!")
print("Collection Name : vehicle_dataset")
print("Persist Folder  : chroma_dataset")
print("=" * 60)