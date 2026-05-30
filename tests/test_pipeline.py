import sys
sys.path.append('src')


def test_chunker_splits_text():
    from chunker import chunk_text
    text = "word " * 200
    chunks = chunk_text(text, chunk_size=100, overlap=20)
    assert len(chunks) > 1, "Long text should produce multiple chunks"
    assert all(len(c.split()) <= 100 for c in chunks), "No chunk should exceed chunk_size"


def test_chunker_short_text():
    from chunker import chunk_text
    text = "Diabetes is a chronic disease that affects millions of people worldwide and requires careful management."
    chunks = chunk_text(text, chunk_size=100, overlap=20)
    assert len(chunks) == 1, "Text under chunk_size should produce exactly one chunk"
    assert len(chunks[0].split()) <= 100, "Single chunk should not exceed chunk_size"


def test_chunk_articles_output_format():
    from chunker import chunk_articles
    articles = [
        {"pmid": "12345", "text": "word " * 150},
        {"pmid": "67890", "text": "word " * 150},
    ]
    chunks = chunk_articles(articles)
    assert len(chunks) > 0, "Should produce chunks"
    assert all("chunk_id" in c for c in chunks), "Every chunk needs a chunk_id"
    assert all("pmid" in c for c in chunks), "Every chunk needs a pmid"
    assert all("text" in c for c in chunks), "Every chunk needs text"


def test_utils_load_json_missing_file():
    from utils import load_json
    result = load_json("data/nonexistent_file.json")
    assert result is None, "Missing file should return None not crash"


def test_utils_clean_text():
    from utils import clean_text
    messy = "  hello    world  \n\n test  "
    result = clean_text(messy)
    assert result == "hello world test", f"Expected clean text, got: {result}"