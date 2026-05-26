import sys
sys.path.append('src')
from rag_chain import ask

questions = [
    "What are the side effects of insulin therapy?",
    "How is Type 2 diabetes diagnosed?",
    "What lifestyle changes help manage diabetes?",
    "What is the role of metformin in diabetes treatment?",
    "Can diabetes be cured completely?",
]

print("="*60)
print("RAG SYSTEM TEST — Healthcare Assistant")
print("="*60)

for i, q in enumerate(questions):
    print(f"\n[Question {i+1}/{len(questions)}]")
    result = ask(q)
    print("\nANSWER:")
    print(result['answer'])
    print("\nSOURCES:")
    print(result['sources_formatted'])
    print(f"\nStats: {result['latency']}s | {result['tokens']} tokens")
    print("-"*60)