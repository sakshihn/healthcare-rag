import sys
sys.path.append('src')
from utils import load_json, save_json, clean_text
import pandas as pd

raw = load_json('data/raw/pubmed_raw.json')
print(f"Loaded {len(raw)} raw articles")

df = pd.DataFrame(raw)
df = df.dropna(subset=['text'])
df['text'] = df['text'].apply(clean_text)
df['word_count'] = df['text'].apply(lambda x: len(x.split()))
df = df[df['word_count'] >= 30]
df = df.drop_duplicates(subset=['text'])
df = df.reset_index(drop=True)

print(f"After cleaning: {len(df)} articles")
print(f"Avg word count: {df['word_count'].mean():.0f}")

articles = df.to_dict(orient='records')
save_json(articles, 'data/processed/articles_clean.json')
print("Real data saved to articles_clean.json")