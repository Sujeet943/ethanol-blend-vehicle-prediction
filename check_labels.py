import joblib

label_encoders = joblib.load("models/label_encoders.pkl")

for col, encoder in label_encoders.items():
    print("=" * 40)
    print(col)
    print(encoder.classes_)