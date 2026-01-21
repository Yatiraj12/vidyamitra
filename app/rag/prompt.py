"""
Prompt Template Module for Vidyamitra
CRP-style prompt engineering for classroom guidance
(Paragraph-based, stable outputs)
"""

from typing import List, Dict


def get_system_message() -> str:
    """
    System instruction for chat-based LLMs
    """
    return (
        "You are Vidyamitra, a digital Cluster Resource Person (CRP) supporting school teachers. "
        "Your role is to provide practical, classroom-ready guidance based on teacher training materials. "
        "Be supportive, clear, and focused on pedagogy and learner understanding. "
        "Avoid policy or administrative discussions."
    )


def get_user_prompt(query: str, context: str) -> str:
    """
    User prompt containing RAG context and teacher query
    """
    return f"""
Context from teacher training materials:
{context}

Teacher's Question:
{query}

Instructions:
- Give a direct, practical answer based on the context
- Focus on classroom teaching strategies
- Use simple language teachers can apply immediately
- End your response with a complete sentence.
- If the context is insufficient, say so briefly and provide general pedagogical guidance
- Keep the response concise (4–6 sentences)

Response:
""".strip()


def get_rag_prompt(query: str, context: str) -> str:
    """
    Backward-compatible combined prompt (for non-chat LLMs)
    """
    return f"""
You are Vidyamitra, a digital Cluster Resource Person (CRP) helping teachers with practical, classroom-ready guidance.

Context from teacher training materials:
{context}

Teacher's Question:
{query}

Instructions:
- Provide clear and actionable teaching guidance
- Keep it classroom-focused and practical
- Avoid administrative or policy language
- Keep the response concise (4–6 sentences)

Response:
""".strip()


def format_context_from_chunks(chunks: List[Dict]) -> str:
    """
    Format retrieved chunks into context string
    """
    if not chunks:
        return "No specific teacher training material was found for this query."

    context_blocks = []

    for i, chunk in enumerate(chunks, start=1):
        text = chunk.get("text", "").strip()
        if text:
            context_blocks.append(f"[Source {i}]\n{text}")

    return "\n\n".join(context_blocks)
