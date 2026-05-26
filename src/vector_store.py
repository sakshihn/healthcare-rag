import sys
sys.path.append('src')

import chromadb
from sentence_transformers import SentenceTransformer
from utils import load_json
import time

CHROMA_PATH = 'data/vectorstore'
COLLECTION_NAME = 'healthcare_rag'
EMBED_MODEL = 'all-MiniLM-L6-v2'
BATCH_SIZE = 50


def build_vector_store():
    print("Loading chunks...")
    chunks = load_json('data/processed/chunks.json')
    print(f"Loaded {len(chunks)} chunks")

    print("\nLoading embedding model...")
    embedder = SentenceTransformer(EMBED_MODEL)
    print("Model loaded")

    print("\nConnecting to ChromaDB...")
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    if COLLECTION_NAME in [c.name for c in client.list_collections()]:
        client.delete_collection(COLLECTION_NAME)
        print("Deleted old collection")

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )
    print(f"Created collection: {COLLECTION_NAME}")

    print(f"\nEmbedding and storing {len(chunks)} chunks...")
    print("This takes 2-5 minutes. Go drink water.\n")

    start = time.time()

    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i:i + BATCH_SIZE]

        texts = [c['text'] for c in batch]
        ids = [c['chunk_id'] for c in batch]
        metadatas = [{
            'pmid': c['pmid'],
            'chunk_index': c['chunk_index'],
            'total_chunks': c['total_chunks']
        } for c in batch]

        embeddings = embedder.encode(texts).tolist()

        collection.add(
            documents=texts,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas
        )

        done = min(i + BATCH_SIZE, len(chunks))
        pct = round(done / len(chunks) * 100)
        elapsed = round(time.time() - start)
        print(f"  {done}/{len(chunks)} chunks stored ({pct}%) — {elapsed}s elapsed")

    total = round(time.time() - start)
    print(f"\nDone! {len(chunks)} chunks stored in {total}s")
    print(f"Vector store saved to: {CHROMA_PATH}/")
    return collection


def load_vector_store():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_collection(COLLECTION_NAME)


if __name__ == '__main__':
    build_vector_store()