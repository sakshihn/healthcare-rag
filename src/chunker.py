import sys
sys.path.append('src')

def chunk_text(text, chunk_size=100, overlap=20):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = ' '.join(words[start:end])
        if len(chunk.strip()) > 30:
            chunks.append(chunk)
        start += (chunk_size - overlap)

    return chunks


def chunk_articles(articles, chunk_size=100, overlap=20):
    all_chunks = []

    for article in articles:
        text = article.get('text', '')
        pmid = article.get('pmid', 'unknown')

        if not text or len(text.split()) < 20:
            continue

        chunks = chunk_text(text, chunk_size, overlap)

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                'text': chunk,
                'pmid': pmid,
                'chunk_id': f"{pmid}_chunk_{i}",
                'chunk_index': i,
                'total_chunks': len(chunks)
            })

    return all_chunks


if __name__ == '__main__':
    from utils import load_json, save_json

    articles = load_json('data/processed/articles_clean.json')
    print(f"Loaded {len(articles)} articles")

    chunks = chunk_articles(articles)
    print(f"Created {len(chunks)} chunks")
    print(f"Avg chunks per article: {len(chunks)/len(articles):.1f}")

    print(f"\nSample chunk:")
    print(f"  ID     : {chunks[0]['chunk_id']}")
    print(f"  Words  : {len(chunks[0]['text'].split())}")
    print(f"  Text   : {chunks[0]['text'][:120]}...")

    save_json(chunks, 'data/processed/chunks.json')
    print(f"\nSaved {len(chunks)} chunks")