import sys
sys.path.append('src')
from simple_vector_store import simple_retrieve

def retrieve(query, n_results=5):
    return simple_retrieve(query, n_results)

if __name__ == '__main__':
    results = retrieve("What is the treatment for Type 2 diabetes?", n_results=3)
    for i, r in enumerate(results):
        print(f"\nResult {i+1} (similarity: {r['similarity']})")
        print(f"PMID: {r['pmid']}")
        print(f"Text: {r['text'][:150]}...")