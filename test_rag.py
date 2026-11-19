from rag.rag_chain import ask_rag

question = "What is E20 fuel?"

answer = ask_rag(question)

print("=" * 80)
print(answer)
print("=" * 80)