from pathlib import Path
import pickle

from langchain_community.retrievers import BM25Retriever


# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CHUNKS_PATH = BASE_DIR / "rag" / "chunks.pkl"


# ==========================================================
# Load Document Chunks
# ==========================================================

if not CHUNKS_PATH.exists():
    raise FileNotFoundError(
        f"Chunks file not found at: {CHUNKS_PATH}"
    )

with open(CHUNKS_PATH, "rb") as f:
    chunks = pickle.load(f)


# ==========================================================
# BM25 Retriever
# ==========================================================

bm25 = BM25Retriever.from_documents(chunks)

bm25.k = 5