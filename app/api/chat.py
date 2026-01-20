"""
Chat API for Vidyamitra
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.rag.rag_pipeline import get_rag_pipeline

router = APIRouter()

# Lazy initialization (created only when needed)
_rag_pipeline = None


def get_pipeline():
    global _rag_pipeline
    if _rag_pipeline is None:
        _rag_pipeline = get_rag_pipeline(llm_provider="groq", top_k=1)
    return _rag_pipeline


class ChatRequest(BaseModel):
    query: str
    language: str = "English"
    return_sources: bool = False


class ChatResponse(BaseModel):
    answer: str
    sources: Optional[list] = None


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    pipeline = get_pipeline()
    return pipeline.query(
        user_query=request.query,
        language=request.language,
        return_sources=request.return_sources,
    )
