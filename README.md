# Healthcare RAG Intelligence System

A production-ready Retrieval Augmented Generation (RAG) system
that answers medical questions using real PubMed research papers
as its knowledge base — with full source citations.

## Live Demo
[Try it here](YOUR_STREAMLIT_URL_HERE)

## What it does
Ask any medical question → the system searches 664 real PubMed
abstracts → retrieves the 5 most relevant chunks using semantic
search → sends them to an LLM → returns a grounded answer with
citations to the exact research papers used.

## Architecture
User Question
    → Semantic Search (sentence-transformers + ChromaDB)
    → Top 5 Relevant Chunks Retrieved
    → Prompt Built with Context + Citations
    → Groq LLaMA 3.3 70B Generates Answer
    → Response with Source PMIDs Returned

## Tech Stack
| Component | Technology |
|-----------|-----------|
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector Store | ChromaDB (persistent, local) |
| LLM | Groq LLaMA 3.3 70B (free tier) |
| RAG Framework | Custom (no LangChain dependency) |
| Backend API | FastAPI + uvicorn |
| Frontend UI | Streamlit |
| Data Source | PubMed API (NCBI Entrez) |

## Project Structure
healthcare-rag/
├── src/
│   ├── ingestion.py      # PubMed data fetching
│   ├── clean_data.py     # pandas cleaning pipeline
│   ├── chunker.py        # text chunking with overlap
│   ├── vector_store.py   # ChromaDB embedding + storage
│   ├── retriever.py      # semantic search
│   ├── prompt.py         # system prompt + formatting
│   ├── rag_chain.py      # full RAG pipeline
│   └── utils.py          # shared helpers
├── api/
│   └── main.py           # FastAPI REST API
├── app/
│   └── chatbot.py        # Streamlit UI
└── data/
    ├── raw/              # downloaded PubMed articles
    └── processed/        # cleaned chunks + vectors

## Results
- 100 PubMed abstracts ingested and cleaned
- 664 chunks stored in vector database
- Average query latency: ~2s end-to-end
- Retrieval similarity scores: 0.55–0.65 on domain queries
- Honest out-of-domain detection (low similarity = says so)

## Setup
1. Clone the repo
2. Create virtual environment: python -m venv .venv
3. Activate: .venv\Scripts\activate (Windows)
4. Install: pip install -r requirements.txt
5. Add GROQ_API_KEY to .env file
6. Build vector store: python src/vector_store.py
7. Run app: streamlit run app/chatbot.py

## API Endpoints
POST /query   — ask a medical question, get cited answer
GET  /health  — server health check
GET  /metrics — query volume and latency stats

Run API: uvicorn api.main:app --host 127.0.0.1 --port 8000
Docs at: http://127.0.0.1:8000/docs