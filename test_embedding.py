from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text")

vector = embeddings.embed_query("What is E20 fuel?")

print(len(vector))
print(vector[:10])