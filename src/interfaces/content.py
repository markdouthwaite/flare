from typing import List
from src.entities.content import RawContent, Content


class RawContentSummarizer:
    def summarize(self, raw_content: RawContent) -> str:
        pass


class RawContentScorer:
    def score(self, raw_content: RawContent) -> float:
        pass


class ContentRepository:
    def create(self, content: Content):
        pass

    def list(self) -> List[Content]:
        pass
