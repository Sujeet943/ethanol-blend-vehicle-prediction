from langchain_community.document_loaders import PyPDFDirectoryLoader

loader = PyPDFDirectoryLoader("documents")
docs = loader.load()

print("Total Pages:", len(docs))

print("=" * 80)

found = False

for doc in docs:
    if "ethanol" in doc.metadata["source"].lower():
        found = True
        print(doc.metadata)
        print(doc.page_content[:500])
        print("=" * 80)

if not found:
    print("❌ ethanol.pdf was NOT loaded.")