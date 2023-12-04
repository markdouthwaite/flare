from typing import Protocol, List, Any
from src.entities.candidate import Candidate


class CandidateRepository(Protocol):
    def get(self, item_id: str) -> Candidate:
        pass

    def list(self, **kwargs) -> List[Candidate]:
        pass

    def rank(self, **kwargs):
        pass

    def list_ids(self, **kwargs) -> List[str]:
        pass

    def list_content_ids(self, **kwargs) -> List[str]:
        pass

    def insert(self, item: Candidate):
        pass

    def update(self, item: Candidate):
        pass

    def delete(self, item: Candidate):
        pass
