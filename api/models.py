from pydantic import BaseModel, Field
from typing import List, Optional


class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Medical question to ask the RAG system"
    )
    n_chunks: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of chunks to retrieve (1-10)"
    )


class SourceItem(BaseModel):
    pmid: str
    similarity: float
    chunk_index: int


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceItem]
    sources_formatted: str
    latency: float
    tokens: int
    chunks_searched: int = 664


class HealthResponse(BaseModel):
    status: str
    model: str
    chunks_in_db: int
    version: str = "1.0.0"