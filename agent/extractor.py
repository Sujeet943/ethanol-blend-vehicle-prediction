import json

from genai.groq_client import ask_groq


# ==========================================================
# Extract Vehicle Information
# ==========================================================

def extract_vehicle_data(question):

    prompt = f"""
You are a vehicle information extraction system.

Extract vehicle information from the user's question.

Return ONLY valid JSON.

Use these exact field names:

Vehicle_Age
Engine_CC
Horsepower
Vehicle_Weight
Transmission
Fuel_Type
Ethanol_Blend
Fuel_Price
Trip_Distance_km
Average_Speed
Engine_RPM
Tire_Pressure_PSI
Maintenance_Status
Road_Type
Traffic_Level
Temperature
Humidity
Weather
AC_Usage
Driving_Style
Passengers

If a value is not provided, return null.

Important rules:

- "5 year old" -> Vehicle_Age = 5
- "1500cc" -> Engine_CC = 1500
- "120 HP" -> Horsepower = 120
- "1200 kg" -> Vehicle_Weight = 1200
- "E20" -> Ethanol_Blend = 20
- "20% ethanol" -> Ethanol_Blend = 20
- "manual" -> Transmission = "Manual"
- "automatic" -> Transmission = "Automatic"
- "petrol" -> Fuel_Type = "Petrol"
- "32 PSI" -> Tire_Pressure_PSI = 32
- "2 passengers" -> Passengers = 2
- "AC on" -> AC_Usage = "Yes"
- "AC off" -> AC_Usage = "No"

User Question:

{question}

Return JSON only.

Example:

{{
    "Vehicle_Age": 5,
    "Engine_CC": 1500,
    "Horsepower": 120,
    "Vehicle_Weight": 1200,
    "Transmission": "Manual",
    "Fuel_Type": "Petrol",
    "Ethanol_Blend": 20,
    "Fuel_Price": null,
    "Trip_Distance_km": null,
    "Average_Speed": null,
    "Engine_RPM": null,
    "Tire_Pressure_PSI": 32,
    "Maintenance_Status": "Good",
    "Road_Type": "City",
    "Traffic_Level": "Medium",
    "Temperature": null,
    "Humidity": null,
    "Weather": "Clear",
    "AC_Usage": "No",
    "Driving_Style": "Normal",
    "Passengers": 2
}}
"""

    response = ask_groq(prompt)

    print("=" * 60)
    print("EXTRACTION RESPONSE")
    print("=" * 60)
    print(response)

    try:

        data = json.loads(response)

        return data

    except json.JSONDecodeError:

        print("Could not parse vehicle information.")

        return None