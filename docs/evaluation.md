# RAG System Evaluation Results

## Test Setup
- 10 domain-specific medical questions
- 1,336 chunks from 200 PubMed abstracts
- Model: Groq LLaMA 3.3 70B
- Embeddings: all-MiniLM-L6-v2

## Results

| Metric | Score |
|--------|-------|
| Citation Rate | 100% |
| Avg Top Similarity | 0.624 |
| Avg Latency | 8.43s |
| Avg Tokens/Query | 1,103 |
| Total Questions Evaluated | 10 |

## Key Findings
- 100% citation rate — zero hallucinations without source grounding
- Strongest retrieval: metformin (0.697), lifestyle changes (0.683)
- Weakest retrieval: HbA1c (0.505) — needs more targeted data