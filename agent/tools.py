# ==========================================================
# Imports
# ==========================================================

from ml.predictor import predict_mileage

from rag.rag_chain import (
    ask_rag,
    retrieve_context
)

from rag.dataset_retriever import search_vehicle

from genai.prompt import create_prompt
from genai.groq_client import ask_groq


# ==========================================================
# Tool 1: Mileage Prediction
# ==========================================================

def mileage_tool(vehicle_data):
    """
    Predict vehicle mileage using the trained CatBoost model.

    Input:
        vehicle_data -> dictionary containing vehicle features

    Output:
        Predicted mileage in km/L
    """

    try:

        prediction = predict_mileage(vehicle_data)

        return prediction

    except Exception as e:

        return f"Error during mileage prediction: {e}"


# ==========================================================
# Tool 2: Knowledge Question
# ==========================================================

def knowledge_tool(question):
    """
    Answer general vehicle knowledge questions
    using the Hybrid RAG pipeline.

    Flow:

        Question
           ↓
        BM25 + ChromaDB
           ↓
        Relevant documents
           ↓
        Groq LLM
           ↓
        Answer + Sources
    """

    try:

        answer = ask_rag(question)

        return answer

    except Exception as e:

        return f"Error during knowledge retrieval: {e}"


# ==========================================================
# Tool 3: Dataset Search
# ==========================================================

def dataset_tool(question):
    """
    Search the vehicle mileage dataset.

    Examples:

        What is the average mileage of Honda City?

        What is the minimum mileage of Honda City?

        What is the maximum mileage of Honda City?

        How many Honda City records are present?
    """

    try:

        result = search_vehicle(question)

        return result

    except Exception as e:

        return f"Error during dataset search: {e}"


# ==========================================================
# Tool 4: Explain Mileage Prediction
# ==========================================================

def explanation_tool(vehicle_data):
    """
    Predict mileage and explain the prediction
    using CatBoost + RAG + Groq.

    Flow:

        Vehicle Data
             ↓
        CatBoost Prediction
             ↓
        Create Retrieval Question
             ↓
        Hybrid RAG Retrieval
             ↓
        Relevant Context
             ↓
        Groq LLM
             ↓
        Final Explanation
    """

    try:

        # --------------------------------------------------
        # Step 1: Predict Mileage
        # --------------------------------------------------

        predicted = predict_mileage(vehicle_data)

        print("=" * 60)
        print("Explanation Tool")
        print("=" * 60)

        print(
            f"Predicted Mileage: {predicted:.2f} km/L"
        )

        # --------------------------------------------------
        # Step 2: Create Retrieval Question
        # --------------------------------------------------

        retrieval_question = f"""
Explain the mileage prediction for this vehicle.

Vehicle Details:

{vehicle_data}

Predicted Mileage:

{predicted:.2f} km/L

Use the available vehicle knowledge documents to explain:

1. Factors affecting mileage
2. Effect of ethanol blend
3. Effect of vehicle weight
4. Effect of engine CC and horsepower
5. Effect of driving conditions
6. Effect of traffic
7. Effect of road type
8. Effect of vehicle maintenance
9. Fuel-saving recommendations
10. Maintenance recommendations

Only use information supported by the retrieved documents.
"""

        # --------------------------------------------------
        # Step 3: Retrieve RAG Context
        # --------------------------------------------------

        context, sources = retrieve_context(
            retrieval_question,
            max_chunks=6
        )

        # --------------------------------------------------
        # Check Context
        # --------------------------------------------------

        if not context:

            return f"""
Predicted Mileage: {predicted:.2f} km/L

I was able to generate the mileage prediction, but
I could not find enough relevant information in the
knowledge base to explain the prediction.
"""

        # --------------------------------------------------
        # Step 4: Create Prompt
        # --------------------------------------------------

        prompt = create_prompt(
            vehicle_data=vehicle_data,
            prediction=predicted,
            context=context
        )

        # --------------------------------------------------
        # Step 5: Generate Final Answer
        # --------------------------------------------------

        answer = ask_groq(prompt)

        # --------------------------------------------------
        # Step 6: Add Sources
        # --------------------------------------------------

        if sources:

            unique_sources = list(
                dict.fromkeys(sources)
            )

            answer += "\n\n-------------------------\n"
            answer += "Sources:\n"

            for source in unique_sources:

                answer += f"• {source}\n"

        # --------------------------------------------------
        # Return Final Answer
        # --------------------------------------------------

        return answer

    except Exception as e:

        return f"Error during explanation generation: {e}"