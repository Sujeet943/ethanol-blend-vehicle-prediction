from agent.tools import (
    mileage_tool,
    knowledge_tool,
    explanation_tool
)


def route(user_query, vehicle_data=None):
    """
    Decide which tool to call based on the user's query.
    """

    query = user_query.lower()

    # Prediction requests
    if any(word in query for word in [
        "predict",
        "mileage",
        "fuel economy",
        "km/l",
        "kmpl"
    ]):
        return mileage_tool(vehicle_data)

    # Explanation requests
    elif any(word in query for word in [
        "explain",
        "why",
        "reason",
        "analysis",
        "improve",
        "tips"
    ]):
        return explanation_tool(vehicle_data)

    # Everything else goes to RAG
    else:
        return knowledge_tool(user_query)