from typing import Protocol, Iterable
from src.entities import ExtractedItem, Post


class ExtractedItemFilter(Protocol):
    def __call__(self, item: ExtractedItem) -> bool:
        pass


class ExtractedItemRepository(Protocol):
    def get(self) -> Iterable[ExtractedItem]:
        pass


class PostRepository(Protocol):
    def get(self) -> Post:
        pass

    def list(self) -> Iterable[Post]:
        pass

    def insert(self, post: Post):
        pass

    def insert_many(self, posts: Iterable[Post]):
        pass