import json
from dataclasses import asdict
from pathlib import Path

from flare.common.errors import FeedRepositoryReadError, FeedRepositoryWriteError
from flare.entities.feeds import Feed


class LocalFeedRepository:
    def __init__(self, path: str):
        self.path = Path(path)

    def get(self, name: str) -> Feed:
        feed_path = self._path(name)
        if not feed_path.exists():
            raise FeedRepositoryReadError(f"no such feed '{name}' found")
        else:
            with feed_path.open("r") as feed_file:
                feed = Feed(**json.load(feed_file))

            return feed

    def exists(self, name: str) -> bool:
        return self._path(name).exists()

    def _path(self, name: str):
        return self.path / (name + ".json")

    def create(self, name: str, feed: Feed):
        feed_path = self._path(name)
        if feed_path.exists():
            raise FeedRepositoryWriteError(
                f"cannot create feed: a feed with name '{name}' already exists"
            )

        with feed_path.open("w") as feed_file:
            json.dump(asdict(feed), feed_file, default=str, indent=4)

    def update(self, name: str, feed: Feed):
        feed_path = self._path(name)
        if not feed_path.exists():
            raise FeedRepositoryWriteError(
                f"cannot update feed: a feed with name '{name}' does not exist"
            )

        with feed_path.open("w") as feed_file:
            json.dump(asdict(feed), feed_file, default=str, indent=4)
