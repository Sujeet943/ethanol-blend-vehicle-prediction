from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Load PDFs
loader = PyPDFDirectoryLoader("documents")
docs = loader.load()

# Split PDFs
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(docs)

print("Chunks:", len(chunks))

# Load Ollama Embedding Model
embeddings = OllamaEmbeddings(
    model="embeddinggemma:300m"
)

# Create Vector Database
vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="vector_db"
)

print("Vector Database Created Successfully!")