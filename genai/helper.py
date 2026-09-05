from genai.groq_client import ask_groq


def mileage_explanation(vehicle_data, predicted_mileage):

    prompt = f"""
You are an Automobile AI Expert.

Analyze the following vehicle details and explain the predicted mileage.

Vehicle Details:
{vehicle_data}

Predicted Mileage:
{predicted_mileage:.2f} km/L

Return the response in proper Markdown.

Use the following format:

# 🚗 Vehicle Mileage Analysis

## 1. Mileage Rating
Classify the mileage as:
- Poor
- Average
- Good
- Excellent

Explain why.

## 2. Why this mileage was predicted
Explain in bullet points.

## 3. Positive Factors
Mention all positive factors that improve mileage.

## 4. Negative Factors
Mention all factors reducing mileage.

## 5. Tips to Improve Mileage
Give at least 5 practical suggestions.

## 6. Final Summary
Provide a short conclusion in 2-3 sentences.

Keep the language simple, beginner-friendly, and professional.
Do not mention that you are an AI model.
"""

    return ask_groq(prompt)