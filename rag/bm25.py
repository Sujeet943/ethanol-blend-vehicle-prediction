
from pathlib import Path
import pickle

from langchain_community.retrievers import BM25Retriever


# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CHUNKS_PATH = BASE_DIR / "rag" / "chunks.pkl"


# ==========================================================
# LOAD PUBLIC CHUNKS
# ==========================================================

if not CHUNKS_PATH.exists():

    raise FileNotFoundError(
        f"Public chunks file not found: {CHUNKS_PATH}"
    )


with open(CHUNKS_PATH, "rb") as f:

    chunks = pickle.load(f)


# ==========================================================
# ACCESS CONTROL
# ==========================================================

public_chunks = []

for chunk in chunks:

    access_level = chunk.metadata.get("access_level")

    # Allow only explicitly public documents
    if access_level == "public":

        public_chunks.append(chunk)


if not public_chunks:

    raise ValueError(
        "No public chunks available for BM25 retrieval."
    )


# ==========================================================
# CREATE BM25 RETRIEVER
# ==========================================================

bm25 = BM25Retriever.from_documents(
    public_chunks
)

bm25.k = 5


# ==========================================================
# STATUS
# ==========================================================

print("BM25 Retriever Loaded Successfully")
print("Total public chunks:", len(public_chunks))
