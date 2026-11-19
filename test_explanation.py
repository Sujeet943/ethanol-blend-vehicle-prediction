from agent.tools import explanation_tool

vehicle_data = {
    "Vehicle_Age": 5,
    "Engine_CC": 1200,
    "Horsepower": 90,
    "Vehicle_Weight": 1100,
    "Transmission": "Manual",
    "Fuel_Type": "Petrol",
    "Ethanol_Blend": 20.0,
    "Fuel_Price": 105,
    "Trip_Distance_km": 120,
    "Average_Speed": 55,
    "Engine_RPM": 2500,
    "Tire_Pressure_PSI": 32,
    "Maintenance_Status": "Good",
    "Road_Type": "Highway",
    "Traffic_Level": "Low",
    "Temperature": 28,
    "Humidity": 60,
    "Weather": "Clear",
    "AC_Usage": "Yes",
    "Driving_Style": "Smooth",
    "Passengers": 2
}

answer = explanation_tool(vehicle_data)

print("=" * 80)
print(answer)
print("=" * 80)