import sys
sys.path.append('src')

from sentence_transformers import SentenceTransformer
from vector_store import load_vector_store

EMBED_MODEL = 'all-MiniLM-L6-v2'
embedder = SentenceTransformer(EMBED_MODEL)


def retrieve(query, n_results=5):
    collection = load_vector_store()

    query_embedding = embedder.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
        include=['documents', 'metadatas', 'distances']
    )

    chunks = []
    for i in range(len(results['documents'][0])):
        chunks.append({
            'text': results['documents'][0][i],
            'pmid': results['metadatas'][0][i]['pmid'],
            'chunk_index': results['metadatas'][0][i]['chunk_index'],
            'similarity': round(1 - results['distances'][0][i], 3)
        })

    return chunks


if __name__ == '__main__':
    queries = [
        "What is the treatment for Type 2 diabetes?",
        "How does insulin resistance work?",
        "Cancer screening methods for early detection",
    ]

    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 60)
        results = retrieve(query, n_results=3)
        for i, r in enumerate(results):
            print(f"\n  Result {i+1} (similarity: {r['similarity']})")
            print(f"  PMID: {r['pmid']}")
            print(f"  Text: {r['text'][:150]}...")