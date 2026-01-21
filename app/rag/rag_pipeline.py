"""
RAG Pipeline Orchestration Module for Vidyamitra
Handles:
- Casual chat
- RAG from CRP material
- Fallback to LLM if data not found
- Translation
"""

from typing import Dict, List
from app.retrieval.vector_store import get_vector_store
from app.rag.llm import get_llm
from app.rag.prompt import (
    get_system_message,
    get_user_prompt,
    format_context_from_chunks,
)


def is_casual_query(query: str) -> bool:
    casual_phrases = {
        "hi", "hello", "hey",
        "thanks", "thank you",
        "good morning", "good evening"
    }
    q = query.lower().strip()
    return q in casual_phrases or len(q.split()) <= 2


class RAGPipeline:
    def __init__(self, llm_provider: str = "groq", top_k: int = 1):
        self.vector_store = get_vector_store()
        self.llm = get_llm(provider=llm_provider)
        self.top_k = top_k

    def query(
        self,
        user_query: str,
        language: str = "English",
        return_sources: bool = False,
    ) -> Dict:

        # 1️⃣ Casual conversation
        if is_casual_query(user_query):
            answer = (
                "Hello! I am Vidyamitra. "
                "I can help you with classroom teaching, "
                "student learning challenges, and practical teaching strategies."
            )
            return {
                "answer": self.llm.translate(answer, language),
                "sources": None,
            }

        # 2️⃣ Retrieval (SAFE)
        retrieved_chunks = []
        try:
            retrieved_chunks = self.vector_store.search(
                user_query, top_k=self.top_k
            )
        except Exception:
            retrieved_chunks = []

        # 3️⃣ Context handling
        if retrieved_chunks:
            context = format_context_from_chunks(retrieved_chunks)
        else:
            context = (
                "No specific training material was found. "
                "Answer using general classroom teaching best practices."
            )

        # 4️⃣ Prompt
        system_message = get_system_message()
        user_prompt = get_user_prompt(user_query, context)
        final_prompt = f"{system_message}\n\n{user_prompt}"

        # 5️⃣ LLM generation
        answer = self.llm.generate(
            final_prompt,
            temperature=0.3,
            max_tokens=350,
        )

        # 6️⃣ Translation
        answer = self.llm.translate(answer, language)

        response = {"answer": answer}

        if return_sources and retrieved_chunks:
            response["sources"] = [
                {
                    "text": c.get("text", "")[:200] + "...",
                    "metadata": c.get("metadata", {}),
                    "score": c.get("score", 0),
                }
                for c in retrieved_chunks
            ]

        return response


def get_rag_pipeline(llm_provider: str = "groq", top_k: int = 1):
    return RAGPipeline(llm_provider=llm_provider, top_k=top_k)
