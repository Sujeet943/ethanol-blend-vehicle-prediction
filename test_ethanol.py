from rag.retriever import retriever

docs = retriever.invoke("ethanol")

print("=" * 80)

for i, doc in enumerate(docs):
    print(f"Document {i+1}")
    print("=" * 80)
    print(doc.metadata)
    print(doc.page_content[:500])
    print()