_embedder = None

def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBED_MODEL)
    return _embedder

def simple_retrieve(query, n_results=5):
    embedder = get_embedder()
    embeddings, chunks = load_simple_store()
    query_embedding = embedder.encode([query])[0]
    similarities = np.dot(embeddings, query_embedding) / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding)
    )
    top_indices = np.argsort(similarities)[::-1][:n_results]
    results = []
    for i in top_indices:
        results.append({
            'text': chunks[i]['text'],
            'pmid': chunks[i]['pmid'],
            'chunk_index': chunks[i]['chunk_index'],
            'similarity': round(float(similarities[i]), 3)
        })
    return results