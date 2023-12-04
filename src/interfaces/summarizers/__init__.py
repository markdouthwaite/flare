from typing import Protocol


class Summarize(Protocol):
    def __init__(self, **kwargs):
        pass

    def summarize(self, system_prompt: str, text: str) -> int:
        pass
