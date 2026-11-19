from ml.predictor import predict_mileage

vehicle = {
    "Vehicle_Age": 5,
    "Engine_CC": 1200,
    "Horsepower": 95,
    "Vehicle_Weight": 1100,
    "Transmission": "Manual",
    "Ethanol_Blend": 20,
    "Fuel_Price": 104,
    "Trip_Distance_km": 150,
    "Average_Speed": 65,
    "Engine_RPM": 2400,
    "Tire_Pressure_PSI": 32,
    "Maintenance_Status": "Good",
    "Road_Type": "City",
    "Traffic_Level": "High",
    "Temperature": 30,
    "Humidity": 60,
    "Weather": "Clear",
    "AC_Usage": "Yes",
    "Driving_Style": "Normal",
    "Passengers": 3
}

print(predict_mileage(vehicle))