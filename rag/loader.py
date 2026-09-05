import os
from langchain_community.document_loaders import PyPDFDirectoryLoader

print("Current Directory:", os.getcwd())

loader = PyPDFDirectoryLoader("documents")

docs = loader.load()

print("Pages:", len(docs))