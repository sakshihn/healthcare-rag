import sys
sys.path.append('src')

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import time
from rag_chain import ask

app = FastAPI(
    title="Healthcare RAG API",
    description="Ask medical questions answered from PubMed research",
    version="1.0.0"
)

query_log = []


class QueryRequest(BaseModel):
    question: str
    n_chunks: Optional[int] = 5


class QueryResponse(BaseModel):
    answer: str
    sources: str
    latency: float
    tokens: int
    chunks_searched: int


class HealthResponse(BaseModel):
    status: str
    total_queries: int
    uptime_seconds: float


START_TIME = time.time()


@app.get("/health", response_model=HealthResponse)
def health_check():
    return {
        "status": "healthy",
        "total_queries": len(query_log),
        "uptime_seconds": round(time.time() - START_TIME, 1)
    }


@app.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    if len(request.question) > 500:
        raise HTTPException(status_code=400, detail="Question too long (max 500 chars)")

    try:
        result = ask(request.question, n_chunks=request.n_chunks)
        query_log.append({
            "question": request.question,
            "latency": result["latency"],
            "tokens": result["tokens"],
            "timestamp": time.time()
        })
        return {
            "answer": result["answer"],
            "sources": result["sources_formatted"],
            "latency": result["latency"],
            "tokens": result["tokens"],
            "chunks_searched": 664
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
def get_metrics():
    if not query_log:
        return {"message": "No queries yet"}

    avg_latency = round(
        sum(q["latency"] for q in query_log) / len(query_log), 2
    )
    total_tokens = sum(q["tokens"] for q in query_log)

    return {
        "total_queries": len(query_log),
        "avg_latency_seconds": avg_latency,
        "total_tokens_used": total_tokens,
        "recent_questions": [
            q["question"] for q in query_log[-5:]
        ]
    }