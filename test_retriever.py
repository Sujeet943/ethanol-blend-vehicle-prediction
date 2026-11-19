from rag.retriever import retrieve

docs = retrieve("What is E20 fuel?")

for i, doc in enumerate(docs, 1):
    print("=" * 80)
    print(f"Document {i}")
    print("=" * 80)
    print(doc.metadata)
    print()
    print(doc.page_content)