"""
LLM Configuration Module for Vidyamitra
Supports Groq with Qwen models
Ensures clean, teacher-facing output and proper translation
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
            raise ValueError("Only Groq provider is supported currently")

        api_key = api_key or os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment")

        self.client = Groq(api_key=api_key)
        self.model_name = model_name or "qwen/qwen3-32b"

    def _clean_response(self, text: str) -> str:
        """
        Remove internal reasoning, meta text, and formatting artifacts
        """
        # Remove <think>...</think>
        text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

        # Remove common meta-reasoning lines
        meta_patterns = [
            r"^okay[, ]+.*$",
            r"^let me .*?$",
            r"^i will .*?$",
            r"^the user .*?$",
            r"^this is general guidance.*$",
            r"^translation.*$",
            r"^here is .*?answer.*$",
        ]

        for pattern in meta_patterns:
            text = re.sub(
                pattern,
                "",
                text,
                flags=re.IGNORECASE | re.MULTILINE,
            )

        # Remove excessive blank lines
        text = re.sub(r"\n{2,}", "\n", text)

        return text.strip()

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
                        "You are Vidyamitra, a digital Cluster Resource Person (CRP) "
                        "supporting school teachers with clear, classroom-ready guidance. "
                        "Do not explain your reasoning. Provide only the final answer."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        raw_output = response.choices[0].message.content.strip()
        return self._clean_response(raw_output)

    def translate(self, text: str, target_language: str) -> str:
        """
        Translate text into Kannada or Hindi.
        Output must be ONLY the final translated text.
        """
        if target_language.lower() == "english":
            return text

        translation_prompt = f"""
You are a professional translator for teachers.

STRICT RULES:
- Translate the FULL text into {target_language}
- Output ONLY the translated text
- DO NOT explain the translation
- DO NOT think aloud
- DO NOT include English text unless unavoidable
- Return a single clean paragraph

Text to translate:
{text}
""".strip()

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a translation engine. "
                        "Output only the translated text."
                    ),
                },
                {
                    "role": "user",
                    "content": translation_prompt,
                },
            ],
            temperature=0.1,
            max_tokens=400,
        )

        raw_output = response.choices[0].message.content.strip()
        return self._clean_response(raw_output)


def get_llm(provider: str = "groq"):
    return LLMConfig(provider=provider)
