import sys
sys.path.append('src')
import time
from rag_chain import ask

test_questions = [
    "What is the role of metformin in diabetes treatment?",
    "What lifestyle changes help manage Type 2 diabetes?",
    "How does insulin resistance develop?",
    "What are the complications of untreated diabetes?",
    "How effective is exercise in controlling blood sugar?",
    "What is HbA1c and why is it important?",
    "What dietary changes help diabetic patients?",
    "How does obesity relate to Type 2 diabetes?",
    "What medications are used besides metformin?",
    "Can Type 2 diabetes be reversed?",
]

print("="*60)
print("RAG SYSTEM EVALUATION")
print("="*60)

results = []
for i, q in enumerate(test_questions):
    print(f"\n[{i+1}/{len(test_questions)}] {q}")
    start = time.time()
    result = ask(q)
    latency = result['latency']
    top_similarity = result['sources'][0]['similarity'] if result['sources'] else 0
    avg_similarity = round(sum(s['similarity'] for s in result['sources']) / len(result['sources']), 3) if result['sources'] else 0
    has_citation = "(Source" in result['answer']
    answer_length = len(result['answer'].split())

    results.append({
        'question': q,
        'latency': latency,
        'top_similarity': top_similarity,
        'avg_similarity': avg_similarity,
        'has_citation': has_citation,
        'answer_length': answer_length,
        'tokens': result['tokens']
    })

    print(f"  Latency: {latency}s | Top similarity: {top_similarity} | Citations: {has_citation}")

print("\n" + "="*60)
print("EVALUATION SUMMARY")
print("="*60)
avg_latency = round(sum(r['latency'] for r in results) / len(results), 2)
avg_top_sim = round(sum(r['top_similarity'] for r in results) / len(results), 3)
citation_rate = round(sum(1 for r in results if r['has_citation']) / len(results) * 100)
avg_tokens = round(sum(r['tokens'] for r in results) / len(results))

print(f"Total questions    : {len(results)}")
print(f"Avg latency        : {avg_latency}s")
print(f"Avg top similarity : {avg_top_sim}")
print(f"Citation rate      : {citation_rate}%")
print(f"Avg tokens/query   : {avg_tokens}")
print("="*60)