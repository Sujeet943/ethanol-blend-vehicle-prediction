from rag.bm25 import bm25_search

docs = bm25_search("What is E20 fuel?")

for i, doc in enumerate(docs, 1):

    print("=" * 80)

    print(i)

    print(doc.metadata["filename"])

    print(doc.page_content[:400])