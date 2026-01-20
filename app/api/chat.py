from fastapi import APIRouter
from pydantic import BaseModel
from app.rag.rag_pipeline import get_rag_pipeline

router = APIRouter(prefix="/chat", tags=["chat"])

rag_pipeline = get_rag_pipeline()


class ChatRequest(BaseModel):
    query: str
    language: str = "English"
    return_sources: bool = False


@router.post("")
def chat(request: ChatRequest):
    result = rag_pipeline.query(
        user_query=request.query,
        language=request.language,
        return_sources=request.return_sources,
    )
    return result
