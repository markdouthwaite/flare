from typing import Optional


class IdentitySummarizer:
    def __init__(self, max_chars: Optional[int] = None):
        self.max_chars = max_chars

    def summarize(self, text: str) -> str:
        if self.max_chars is not None:
            text = text[: self.max_chars]
        return text
