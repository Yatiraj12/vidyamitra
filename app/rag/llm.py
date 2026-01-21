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
        cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
        return cleaned.strip()

    def generate(
        self,
        prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 300,
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

        # 🛡️ Safety fallback (prevents blank answers)
        if not cleaned or len(cleaned) < 20:
            return (
                "To address this in class, use simple examples, hands-on activities, "
                "and regular student interaction to reinforce understanding."
            )

        return cleaned

    def translate(self, text: str, target_language: str) -> str:
        if target_language.lower() == "english":
            return text

        prompt = f"""
Translate the following text into {target_language}.
Return only the translated text.

Text:
{text}
""".strip()

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=450,
        )

        raw = response.choices[0].message.content or ""
        return self._clean_response(raw)


def get_llm(provider: str = "groq"):
    return LLMConfig(provider=provider)
