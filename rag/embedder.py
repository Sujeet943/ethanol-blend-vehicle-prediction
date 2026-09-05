from pathlib import Path
import pickle
import shutil

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DOCUMENTS_PATH = BASE_DIR / "documents"
VECTOR_DB_PATH = BASE_DIR / "vector_db"
CHUNKS_PATH = BASE_DIR / "rag" / "chunks.pkl"


# ==========================================================
# Configuration
# ==========================================================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 700
CHUNK_OVERLAP = 100


# ==========================================================
# Delete Existing Vector Database
# ==========================================================

if VECTOR_DB_PATH.exists():
    shutil.rmtree(VECTOR_DB_PATH)
    print("Old Vector Database deleted.")


# ==========================================================
# Load PDF Documents
# ==========================================================

loader = PyPDFDirectoryLoader(str(DOCUMENTS_PATH))

documents = loader.load()

print(f"Loaded Pages : {len(documents)}")


if not documents:
    raise ValueError(
        f"No PDF documents found in: {DOCUMENTS_PATH}"
    )


# ==========================================================
# Improve Metadata
# ==========================================================

for doc in documents:

    file_path = Path(doc.metadata["source"])

    doc.metadata["filename"] = file_path.name

    doc.metadata["title"] = file_path.stem.replace("_", " ")


# ==========================================================
# Split Documents
# ==========================================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)

chunks = splitter.split_documents(documents)

print(f"Chunks Created : {len(chunks)}")


# ==========================================================
# Hugging Face Embedding Model
# ==========================================================

print("\nLoading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)

print("Embedding model loaded successfully.")


# ==========================================================
# Create Chroma Vector Database
# ==========================================================

print("\nCreating Chroma Vector Database...")

vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=str(VECTOR_DB_PATH)
)

print("\nVector Database Created Successfully!")
print(f"Stored {len(chunks)} chunks.")


# ==========================================================
# Save Chunks for BM25
# ==========================================================

with open(CHUNKS_PATH, "wb") as f:
    pickle.dump(chunks, f)

print("Chunks saved for BM25.")


# ==========================================================
# Show Sample Metadata
# ==========================================================

print("\nSample Metadata:")
print(chunks[0].metadata)