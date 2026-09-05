from rag.logger import logger
from rag.retriever import retrieve
from rag.dataset_retriever import search_vehicle
from genai.groq_client import ask_groq

from rag.memory import (
    add_message,
    get_history
)


# ==========================================================
# Retrieve Documents
# ==========================================================

def retrieve_documents(question):
    """
    Returns Document objects from the Hybrid Retriever.

    Hybrid Retriever:
        1. ChromaDB semantic search
        2. BM25 keyword search
    """

    docs = retrieve(question)

    return docs


# ==========================================================
# Build Context + Sources
# ==========================================================

def retrieve_context(question, max_chunks=6):
    """
    Builds the final context for the LLM.

    Sources:
        1. PDF RAG
           - ChromaDB
           - BM25

        2. Vehicle Mileage Dataset
           - Pandas
           - Vehicle/model search

    Returns:
        context
        sources
    """

    # ======================================================
    # PDF RAG
    # ======================================================

    docs = retrieve_documents(question)

    logger.info(
        f"Retrieved {len(docs)} PDF documents."
    )

    seen = set()

    context_chunks = []

    sources = []


    # ======================================================
    # Process PDF Documents
    # ======================================================

    for doc in docs:

        text = doc.page_content.strip()

        # Remove duplicate chunks
        if text in seen:
            continue

        seen.add(text)

        context_chunks.append(text)

        # --------------------------------------------------
        # Source
        # --------------------------------------------------

        source = doc.metadata.get(
            "source",
            "Unknown"
        )

        # LangChain PDF page is usually 0-based
        page = doc.metadata.get(
            "page",
            0
        ) + 1

        sources.append(
            f"{source} (Page {page})"
        )

        # Limit PDF chunks
        if len(context_chunks) >= max_chunks:
            break


    # ======================================================
    # Vehicle Dataset Search
    # ======================================================

    dataset_context = search_vehicle(question)


    # ======================================================
    # Add Dataset Context
    # ======================================================

    if dataset_context:

        logger.info(
            "Vehicle dataset information found."
        )

        context_chunks.append(
            "VEHICLE DATASET INFORMATION:\n"
            + dataset_context
        )

        sources.append(
            "Vehicle Mileage Dataset"
        )

    else:

        logger.info(
            "No vehicle-specific dataset information found."
        )


    # ======================================================
    # Check Context
    # ======================================================

    if not context_chunks:

        logger.warning(
            "No relevant documents or dataset records found."
        )

        return "", []


    # ======================================================
    # Combine Context
    # ======================================================

    context = "\n\n".join(
        context_chunks
    )


    return context, sources


# ==========================================================
# Full RAG Pipeline
# ==========================================================

def ask_rag(question):

    logger.info("=" * 80)

    logger.info(
        f"New Question : {question}"
    )


    # ======================================================
    # Save User Question
    # ======================================================

    add_message(
        "User",
        question
    )


    # ======================================================
    # Retrieve Context
    # ======================================================

    context, sources = retrieve_context(
        question
    )


    # ======================================================
    # No Context Found
    # ======================================================

    if context == "":

        logger.warning(
            "No context retrieved."
        )

        answer = (
            "I couldn't find this information "
            "in the provided documents or dataset."
        )

        add_message(
            "Assistant",
            answer
        )

        return answer


    # ======================================================
    # Conversation History
    # ======================================================

    history = get_history()


    # ======================================================
    # Prompt
    # ======================================================

    prompt = f"""
You are an expert Automobile AI Assistant.

You answer questions using ONLY the information provided
in the CONTEXT below.

==========================================================
IMPORTANT RULES
==========================================================

1. Use ONLY the provided context.

2. Never invent information.

3. Never invent mileage values.

4. Never invent vehicle specifications.

5. If vehicle-specific information is available in the
   VEHICLE DATASET INFORMATION section, use it.

6. If multiple records exist for the same vehicle/model,
   do NOT present one record as the vehicle's fixed mileage.

7. For vehicle mileage questions, use the dataset summary
   such as:
   - Number of records
   - Average mileage
   - Minimum mileage
   - Maximum mileage

8. Explain that dataset mileage can vary because of:
   - Engine CC
   - Horsepower
   - Vehicle weight
   - Ethanol blend
   - Average speed
   - Traffic level
   - Driving style
   - AC usage
   - Tyre pressure
   - Road type
   - Weather
   - Maintenance

   ONLY mention these factors when they are supported by
   the provided context.

9. Dataset mileage represents observed values from the
   project dataset. Do not call it the manufacturer's
   official mileage.

10. Use PDF information for general automobile knowledge.

11. If information is not available, say:

"I couldn't find this information in the provided
documents or dataset."

12. Never use outside knowledge.

13. Use conversation history to understand follow-up
    questions.

14. Keep answers clear and easy to understand.

15. Use bullet points whenever appropriate.

16. Clearly distinguish between:

    - General information from PDFs
    - Vehicle information from the dataset
    - ML predictions

17. If the user asks for a prediction, do not invent a
    prediction from the dataset. The ML prediction model
    should be used when required input features are
    available.

==========================================================
CONVERSATION HISTORY
==========================================================

{history}


==========================================================
CONTEXT
==========================================================

{context}


==========================================================
USER QUESTION
==========================================================

{question}

"""


    # ======================================================
    # Send Prompt to Groq
    # ======================================================

    try:

        answer = ask_groq(
            prompt
        )

        logger.info(
            "Answer generated successfully."
        )

    except Exception as e:

        logger.error(
            f"Groq Error : {e}"
        )

        return f"Error : {e}"


    # ======================================================
    # Save Assistant Response
    # ======================================================

    add_message(
        "Assistant",
        answer
    )


    # ======================================================
    # Remove Duplicate Sources
    # ======================================================

    unique_sources = list(
        dict.fromkeys(sources)
    )


    # ======================================================
    # Add Sources to Answer
    # ======================================================

    if unique_sources:

        answer += (
            "\n\n"
            "-------------------------\n"
            "Sources:\n"
        )

        for src in unique_sources:

            answer += f"• {src}\n"


    # ======================================================
    # Logging
    # ======================================================

    logger.info(
        "Response returned to user."
    )

    logger.info("=" * 80)


    return answer