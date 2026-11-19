from rag.rag_chain import retrieve_context

context = retrieve_context("What is E20 fuel?")

print("=" * 80)
print("Retrieved Context")
print("=" * 80)
print(context)