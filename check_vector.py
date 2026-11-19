from rag.retriever import vectordb

collection = vectordb._collection

print("=" * 80)
print("Total Chunks Stored:", collection.count())
print("=" * 80)

results = collection.get()

docs = results["documents"]
metadatas = results["metadatas"]

found = False

for doc, meta in zip(docs, metadatas):
    if "ethanol.pdf" in meta.get("source", "").lower():
        found = True
        print("=" * 80)
        print(meta)
        print(doc[:600])
        print("=" * 80)

if not found:
    print("❌ No chunks from ethanol.pdf found in ChromaDB.")