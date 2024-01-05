from typing import Protocol
from src.entities.feeds import Feed


class FeedRepository(Protocol):
    def get(self, name: str) -> Feed:
        pass

    def create(self, name: str, feed: Feed):
        pass

    def update(self, name: str, feed: Feed):
        pass

    def exists(self, name: str) -> bool:
        pass
