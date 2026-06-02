import numpy as np
import json
import os
import sys
sys.path.append('src')
from sentence_transformers import SentenceTransformer
from utils import load_json, save_json

STORE_PATH = 'data/vectorstore_simple'
EMBED_MODEL = 'all-MiniLM-L6-v2'

_embedder = None

def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBED_MODEL)
    return _embedder

def load_simple_store():
    embeddings = np.load(f'{STORE_PATH}/embeddings.npy')
    chunks = load_json(f'{STORE_PATH}/chunks.json')
    return embeddings, chunks

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

def build_simple_store():
    os.makedirs(STORE_PATH, exist_ok=True)
    chunks = load_json('data/processed/chunks.json')
    print(f"Embedding {len(chunks)} chunks...")
    embedder = get_embedder()
    texts = [c['text'] for c in chunks]
    embeddings = embedder.encode(texts, show_progress_bar=True)
    np.save(f'{STORE_PATH}/embeddings.npy', embeddings)
    save_json(chunks, f'{STORE_PATH}/chunks.json')
    print(f"Done! Saved {len(chunks)} chunks")

if __name__ == '__main__':
    build_simple_store()