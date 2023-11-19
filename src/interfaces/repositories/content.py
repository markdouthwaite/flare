from typing import Protocol, List, Any, Iterable
from src.entities.content import Content, RawContent


class ContentRepository(Protocol):
    def get(self, content_id: str) -> Content:
        pass

    def list(self, **kwargs) -> List[Content]:
        pass

    def insert(self, content: Content):
        pass

    def delete(self):
        pass

    def search(self, query_text: str, limit: int = 10, **kwargs: Any) -> List[Content]:
        pass

    def similar(self, content_id: str, limit: int = 10) -> List[Content]:
        pass


class RawContentRepository(Protocol):
    def iter(self, **kwargs) -> Iterable[RawContent]:
        pass
