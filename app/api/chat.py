from fastapi import APIRouter
from pydantic import BaseModel
from app.rag.rag_pipeline import get_rag_pipeline

# Create router (NO prefix here)
router = APIRouter()

# Initialize RAG pipeline once
rag_pipeline = get_rag_pipeline()


class ChatRequest(BaseModel):
    query: str
    language: str = "English"
    return_sources: bool = False


@router.post("/chat")
def chat(request: ChatRequest):
    """
    Main chat endpoint for Vidyamitra
    """
    return rag_pipeline.query(
        user_query=request.query,
        language=request.language,
        return_sources=request.return_sources,
    )
