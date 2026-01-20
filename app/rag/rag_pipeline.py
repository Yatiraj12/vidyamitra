"""
RAG Pipeline Orchestration Module for Vidyamitra
Handles:
- Casual chat
- CRP-style RAG when data exists
- LLM fallback when data is missing
- Language translation
"""

from typing import Dict
from app.retrieval.vector_store import get_vector_store
from app.rag.llm import get_llm
from app.rag.prompt import (
    get_system_message,
    get_user_prompt,
    format_context_from_chunks,
)


def is_casual_query(query: str) -> bool:
    casual_phrases = [
        "hi", "hello", "hey",
        "how are you",
        "good morning", "good evening",
        "thanks", "thank you"
    ]
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
                "I can help you with classroom teaching, student learning challenges, "
                "and practical teaching strategies. "
                "Please ask your question."
            )

            return {
                "answer": self.llm.translate(answer, language),
                "sources": None,
            }

        # 2️⃣ Retrieve chunks
        retrieved_chunks = self.vector_store.search(
            user_query, top_k=self.top_k
        )

        # 3️⃣ Decide: RAG or LLM fallback
        use_rag = (
            retrieved_chunks
            and retrieved_chunks[0].get("score", 0) <= -0.1
        )

        # 4️⃣ RAG PATH (data exists)
        if use_rag:
            context = format_context_from_chunks(retrieved_chunks)

            system_message = get_system_message()
            user_prompt = get_user_prompt(user_query, context)
            final_prompt = f"{system_message}\n\n{user_prompt}"

            answer = self.llm.generate(
                final_prompt,
                temperature=0.3,
                max_tokens=300,
            )

        # 5️⃣ LLM FALLBACK PATH (no data)
        else:
            fallback_prompt = f"""
You are Vidyamitra, a digital Cluster Resource Person (CRP).

The following question is not directly covered in the available
teacher training materials. Provide general, responsible pedagogical
guidance suitable for school teachers.

Teacher's Question:
{user_query}

Instructions:
- Clearly state that this is general guidance
- Keep the advice classroom-focused
- Avoid policy or administrative discussion
- Keep the response concise (4–6 sentences)

Response:
""".strip()

            answer = self.llm.generate(
                fallback_prompt,
                temperature=0.4,
                max_tokens=300,
            )

        # 6️⃣ Translate if needed
        answer = self.llm.translate(answer, language)

        response = {"answer": answer}

        if return_sources:
            response["sources"] = [
                {
                    "text": chunk.get("text", "")[:200] + "...",
                    "metadata": chunk.get("metadata", {}),
                    "score": chunk.get("score", 0),
                }
                for chunk in retrieved_chunks
            ] if use_rag else []

        return response


def get_rag_pipeline(llm_provider: str = "groq", top_k: int = 1):
    return RAGPipeline(llm_provider=llm_provider, top_k=top_k)
