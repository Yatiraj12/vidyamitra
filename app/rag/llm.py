"""
LLM Configuration Module for Vidyamitra
Groq + Qwen support with output cleaning and safety fallback
"""

import os
import re
from groq import Groq


class LLMConfig:
    def __init__(
        self,
        provider: str = "groq",
        api_key: str | None = None,
        model_name: str | None = None,
    ):
        self.provider = provider.lower()

        if self.provider != "groq":
            raise ValueError("Only Groq provider is supported")

        api_key = api_key or os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found")

        self.client = Groq(api_key=api_key)
        self.model_name = model_name or "qwen/qwen3-32b"

    def _clean_response(self, text: str) -> str:
        # Remove Qwen internal reasoning if any
        cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
        return cleaned.strip()

    def generate(
        self,
        prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 450,
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Vidyamitra, a digital Cluster Resource Person (CRP). "
                        "Give clear, practical, classroom-ready guidance to teachers."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        raw = response.choices[0].message.content or ""
        cleaned = self._clean_response(raw)

        # 🛡️ Safety fallback (prevents blank / tiny answers)
        if not cleaned or len(cleaned) < 20:
            return (
                "To address this in class, use simple examples, hands-on activities, "
                "and regular student interaction to reinforce understanding."
            )

        return cleaned

    def translate(self, text: str, target_language: str) -> str:
        """
        STRICT translation for Kannada / Hindi.
        Output MUST be only translated text.
        """

        if target_language.lower() == "english":
            return text

        translation_prompt = f"""
You are a professional educational translator.

Translate the following text into {target_language}.

STRICT RULES:
- Output ONLY the translated text
- DO NOT explain words or sentences
- DO NOT include English words
- DO NOT include examples or commentary
- Use simple, natural language suitable for teachers
- Keep the meaning accurate and complete

Text:
{text}

Translated text:
""".strip()

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict translation engine. Do not add explanations.",
                },
                {
                    "role": "user",
                    "content": translation_prompt,
                },
            ],
            temperature=0.1,
            max_tokens=500,
        )

        raw = response.choices[0].message.content or ""
        return self._clean_response(raw)


def get_llm(provider: str = "groq"):
    return LLMConfig(provider=provider)
