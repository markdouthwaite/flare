import os
from typing import Any, Dict

from openai import OpenAI


class OpenAIScorer:
    model_name = "gpt-4-1106-preview"

    defaults = dict(
        temperature=0.3,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    def __init__(
        self,
        max_chars: int = 1000,
    ):
        self.client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))
        self.max_chars = max_chars

    def score(self, system_prompt: str, text: str) -> int:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text[: self.max_chars]},
            ],
            **self.defaults,
        )
        score = response.choices[0].message.content
        return int(score)