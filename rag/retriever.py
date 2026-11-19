
from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from rag.bm25 import bm25


# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_DB_PATH = BASE_DIR / "vector_db"


# ==========================================================
# LOAD EMBEDDING MODEL
# ==========================================================

print("Loading RAG embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ==========================================================
# LOAD EXISTING CHROMA COLLECTION
# ==========================================================

if not VECTOR_DB_PATH.exists():
    raise FileNotFoundError(
        f"Vector database not found: {VECTOR_DB_PATH}"
    )

vector_db = Chroma(
    collection_name="langchain",
    persist_directory=str(VECTOR_DB_PATH),
    embedding_function=embeddings
)

vector_retriever = vector_db.as_retriever(
    search_kwargs={"k": 5}
)

print("ChromaDB collection loaded:", "langchain")
print("ChromaDB document count:", vector_db._collection.count())


# ==========================================================
# HYBRID RETRIEVAL
# ==========================================================

def retrieve(question: str, k: int = 5):

    if not question or not question.strip():
        return []

    # Semantic vector search
    vector_docs = vector_retriever.invoke(question)

    # BM25 keyword search
    keyword_docs = bm25.invoke(question)

    # Combine results
    combined_docs = vector_docs + keyword_docs

    unique_docs = []
    seen = set()

    for doc in combined_docs:

        # Public-only filtering
        if doc.metadata.get("access_level") != "public":
            continue

        content = doc.page_content.strip()

        if not content or content in seen:
            continue

        seen.add(content)
        unique_docs.append(doc)

    return unique_docs[:k]


print("Hybrid Retriever Loaded Successfully")
