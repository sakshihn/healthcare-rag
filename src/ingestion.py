import requests
import json
import time
import sys
sys.path.append('src')
from utils import save_json, clean_text

def fetch_pubmed_ids(query, max_results=100):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmax": max_results, "retmode": "json"}
    r = requests.get(url, params=params, timeout=15)
    return r.json()["esearchresult"]["idlist"]

def fetch_abstract(pmid):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {"db": "pubmed", "id": pmid, "retmode": "text", "rettype": "abstract"}
    try:
        r = requests.get(url, params=params, timeout=15)
        return {"pmid": pmid, "text": r.text.strip()}
    except Exception as e:
        print(f"Failed {pmid}: {e}")
        return None

if __name__ == "__main__":
    QUERY = "diabetes treatment insulin 2023"
    print(f"Fetching: {QUERY}")
    ids = fetch_pubmed_ids(QUERY, max_results=100)
    print(f"Found {len(ids)} articles")

    articles = []
    for i, pmid in enumerate(ids):
        article = fetch_abstract(pmid)
        if article and len(article["text"]) > 100:
            articles.append(article)
        if (i+1) % 10 == 0:
            print(f"Fetched {i+1}/{len(ids)}")
        time.sleep(0.4)

    save_json(articles, "data/raw/pubmed_raw.json")
    print(f"Done! Saved {len(articles)} real articles")