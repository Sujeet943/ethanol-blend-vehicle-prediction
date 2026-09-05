from pathlib import Path

from rag.bm25 import bm25
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

VECTOR_DB_PATH = BASE_DIR / "vector_db"


# ==========================================================
# Embedding Model
# ==========================================================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)


# ==========================================================
# Chroma Vector Database
# ==========================================================

vectordb = Chroma(
    persist_directory=str(VECTOR_DB_PATH),
    embedding_function=embeddings
)


# ==========================================================
# Vector Retriever
# ==========================================================

retriever = vectordb.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 5
    }
)


# ==========================================================
# Hybrid Retrieval
# ==========================================================

def retrieve(question: str):
    """
    Hybrid Search

    1. Vector Search
    2. BM25 Search
    3. Merge Results
    4. Remove Duplicates
    5. Rank Documents
    6. Return Top Documents
    """

    if not question or not question.strip():
        return []

    # ------------------------------------------------------
    # Vector Search
    # ------------------------------------------------------

    vector_docs = retriever.invoke(question)

    # ------------------------------------------------------
    # BM25 Search
    # ------------------------------------------------------

    keyword_docs = bm25.invoke(question)

    # ------------------------------------------------------
    # Merge Results
    # ------------------------------------------------------

    all_docs = []

    # Vector search gets higher priority
    for doc in vector_docs:
        doc.metadata["score"] = 2
        all_docs.append(doc)

    # BM25 search gets lower priority
    for doc in keyword_docs:
        doc.metadata["score"] = 1
        all_docs.append(doc)

    # ------------------------------------------------------
    # Remove Duplicates
    # ------------------------------------------------------

    merged = {}

    for doc in all_docs:

        key = (
            doc.metadata.get("filename"),
            doc.page_content[:150]
        )

        if key not in merged:
            merged[key] = doc

        else:
            merged[key].metadata["score"] += doc.metadata["score"]

    # ------------------------------------------------------
    # Rank Documents
    # ------------------------------------------------------

    ranked_docs = sorted(
        merged.values(),
        key=lambda d: d.metadata["score"],
        reverse=True
    )

    # ------------------------------------------------------
    # Return Best Documents
    # ------------------------------------------------------

    return ranked_docs[:5]