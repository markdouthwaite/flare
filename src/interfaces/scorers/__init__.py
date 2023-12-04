from typing import Protocol


class Scorer(Protocol):
    def __init__(self, **kwargs):
        pass

    def score(self, system_prompt: str, text: str) -> int:
        pass
