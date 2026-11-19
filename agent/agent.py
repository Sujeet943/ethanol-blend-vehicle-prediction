import json

from genai.groq_client import ask_groq

from agent.tools import (
    mileage_tool,
    knowledge_tool,
    dataset_tool,
    explanation_tool
)


# ==========================================================
# Tool Selection
# ==========================================================

def decide_tool(question):

    question_lower = question.lower().strip()

    # ------------------------------------------------------
    # 1. Prediction + Explanation
    # ------------------------------------------------------

    explanation_keywords = [
        "predict and explain",
        "prediction and explain",
        "predict my mileage and explain",
        "explain my mileage",
        "why is my mileage",
        "why did i get this mileage",
        "why predicted mileage",
        "factors affecting my mileage",
        "predict mileage and tell me why"
    ]

    for keyword in explanation_keywords:

        if keyword in question_lower:
            return "explanation_tool"


    # ------------------------------------------------------
    # 2. Pure Mileage Prediction
    # ------------------------------------------------------

    prediction_keywords = [
        "predict mileage",
        "predict my mileage",
        "mileage prediction",
        "predict fuel efficiency",
        "predict fuel economy",
        "calculate my mileage",
        "what will be my mileage",
        "what is my predicted mileage"
    ]

    for keyword in prediction_keywords:

        if keyword in question_lower:
            return "mileage_tool"


    # ------------------------------------------------------
    # 3. Dataset Questions
    # ------------------------------------------------------

    dataset_keywords = [
        "average mileage",
        "minimum mileage",
        "maximum mileage",
        "number of records",
        "how many records",
        "dataset",
        "average mileage of",
        "mileage of honda",
        "mileage of toyota",
        "mileage of maruti",
        "vehicle records"
    ]

    for keyword in dataset_keywords:

        if keyword in question_lower:
            return "dataset_tool"


    # ------------------------------------------------------
    # 4. Knowledge / RAG Questions
    # ------------------------------------------------------

    knowledge_keywords = [
        "what is",
        "how does",
        "explain ethanol",
        "ethanol blending",
        "fuel economy",
        "fuel efficiency",
        "engine performance",
        "vehicle maintenance",
        "maintenance",
        "driving tips",
        "what affects mileage",
        "how to improve mileage",
        "rag"
    ]

    for keyword in knowledge_keywords:

        if keyword in question_lower:
            return "knowledge_tool"


    # ------------------------------------------------------
    # 5. LLM fallback
    # ------------------------------------------------------

    prompt = f"""
You are a vehicle mileage AI agent.

Available tools:

1. mileage_tool
Use for numerical mileage prediction.

2. explanation_tool
Use for mileage prediction + explanation.

3. dataset_tool
Use for questions about dataset statistics,
vehicle average mileage, minimum, maximum,
number of records, etc.

4. knowledge_tool
Use for general automobile knowledge,
ethanol blending, fuel economy,
maintenance, engine performance, driving tips, etc.

User question:

{question}

Return ONLY valid JSON.

Example:

{{
    "tool": "mileage_tool"
}}

Allowed tools:

mileage_tool
knowledge_tool
dataset_tool
explanation_tool
"""

    try:

        response = ask_groq(prompt)

        print("Agent Decision:", response)

        # Remove markdown code fences if Groq adds them
        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.strip()

        decision = json.loads(response)

        tool = decision.get("tool")

        valid_tools = [
            "mileage_tool",
            "knowledge_tool",
            "dataset_tool",
            "explanation_tool"
        ]

        if tool in valid_tools:

            return tool

    except Exception as e:

        print("Agent decision error:", e)


    # Safe fallback

    return "knowledge_tool"


# ==========================================================
# Vehicle Data Validation
# ==========================================================

REQUIRED_FEATURES = [

    "Vehicle_Age",
    "Engine_CC",
    "Horsepower",
    "Vehicle_Weight",
    "Transmission",
    "Fuel_Type",
    "Ethanol_Blend",
    "Fuel_Price",
    "Trip_Distance_km",
    "Average_Speed",
    "Engine_RPM",
    "Tire_Pressure_PSI",
    "Maintenance_Status",
    "Road_Type",
    "Traffic_Level",
    "Temperature",
    "Humidity",
    "Weather",
    "AC_Usage",
    "Driving_Style",
    "Passengers"
]


def validate_vehicle_data(vehicle_data):

    if vehicle_data is None:

        return False, REQUIRED_FEATURES


    missing = []

    for feature in REQUIRED_FEATURES:

        if feature not in vehicle_data:

            missing.append(feature)

    if missing:

        return False, missing


    return True, []


# ==========================================================
# Main Agent
# ==========================================================

def run_agent(question, vehicle_data=None):

    print("=" * 70)
    print("AGENT STARTED")
    print("=" * 70)

    print("User Question:")
    print(question)

    # ------------------------------------------------------
    # Decide tool
    # ------------------------------------------------------

    tool_name = decide_tool(question)

    print("Selected Tool:", tool_name)

    # ======================================================
    # Mileage Prediction
    # ======================================================

    if tool_name == "mileage_tool":

        valid, missing = validate_vehicle_data(vehicle_data)

        if not valid:

            return (
                "Vehicle information is required for mileage prediction.\n\n"
                "Please provide these details:\n\n"
                + "\n".join(
                    f"• {feature}"
                    for feature in missing
                )
            )

        try:

            print("Executing mileage_tool...")

            prediction = mileage_tool(vehicle_data)

            print(
                f"Mileage Prediction: {prediction}"
            )

            return f"""
## 🚗 Mileage Prediction

**Predicted Mileage: {prediction:.2f} km/L**

The CatBoost regression model predicted this mileage
based on the provided vehicle and operating conditions.
"""

        except Exception as e:

            print("Mileage tool error:", e)

            return f"Error during mileage prediction: {e}"


    # ======================================================
    # Dataset Tool
    # ======================================================

    elif tool_name == "dataset_tool":

        try:

            print("Executing dataset_tool...")

            return dataset_tool(question)

        except Exception as e:

            print("Dataset tool error:", e)

            return f"Error during dataset search: {e}"


    # ======================================================
    # Knowledge Tool / RAG
    # ======================================================

    elif tool_name == "knowledge_tool":

        try:

            print("Executing knowledge_tool...")

            return knowledge_tool(question)

        except Exception as e:

            print("Knowledge tool error:", e)

            return f"Error during knowledge retrieval: {e}"


    # ======================================================
    # Explanation Tool
    # ======================================================

    elif tool_name == "explanation_tool":

        valid, missing = validate_vehicle_data(vehicle_data)

        if not valid:

            return (
                "To predict and explain mileage, "
                "I need the vehicle details.\n\n"
                "Please provide:\n\n"
                + "\n".join(
                    f"• {feature}"
                    for feature in missing
                )
            )

        try:

            print("Executing explanation_tool...")

            answer = explanation_tool(vehicle_data)

            return answer

        except Exception as e:

            print("Explanation tool error:", e)

            return f"Error during explanation: {e}"


    # ======================================================
    # Fallback
    # ======================================================

    return knowledge_tool(question)