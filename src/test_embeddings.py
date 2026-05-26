from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = [
    "Diabetes is treated with insulin therapy",
    "Blood sugar management requires medication",
    "The cat sat on the mat",
    "Football is a popular sport",
]

embeddings = model.encode(sentences)

print(f"Each sentence becomes {len(embeddings[0])} numbers")
print(f"\nFirst 5 numbers of sentence 1:")
print([round(float(x), 4) for x in embeddings[0][:5]])
print(f"\nFirst 5 numbers of sentence 2:")
print([round(float(x), 4) for x in embeddings[1][:5]])
print(f"\nFirst 5 numbers of sentence 4 (sport):")
print([round(float(x), 4) for x in embeddings[3][:5]])