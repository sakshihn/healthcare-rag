import sys
sys.path.append('src')

from sentence_transformers import SentenceTransformer
from vector_store import load_vector_store

EMBED_MODEL = 'all-MiniLM-L6-v2'

_embedder = None
_collection = None

def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBED_MODEL)
    return _embedder

def get_collection():
    global _collection
    if _collection is None:
        _collection = load_vector_store()
    return _collection

def retrieve(query, n_results=5):
    embedder = get_embedder()
    collection = get_collection()

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