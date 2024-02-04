import json
import os
from dataclasses import asdict
from typing import Iterable, Optional

import pandas as pd

from flare.common.errors import PostRepositoryReadError, FeedRepositoryWriteError
from flare.entities import Condition, Post


class ParquetPostRepository:
    def __init__(self, path: str):
        self.path = path
        self.primary_key = "url"

    def list(
        self,
        order_by: str = None,
        where: Optional[Iterable[Condition]] = None,
    ):
        if os.path.exists(self.path):
            df = pd.read_parquet(self.path)
            _posts = df.to_dict(orient="records")
            posts = []
            for post in _posts:
                post["metadata"] = json.loads(post["metadata"])
                posts.append(Post(**post))
        else:
            posts = []
        return posts

    def get(self, post_id: str) -> Post:
        if os.path.exists(self.path):
            df = pd.read_parquet(self.path)
            df = df[df["id"] == post_id]
            _posts = df.to_dict(orient="records")
            if len(_posts) < 1:
                raise PostRepositoryReadError(f"no such post with id '{post_id}'")
            else:
                # check for multiple posts?
                post = _posts[0]
                post["metadata"] = json.loads(post["metadata"])
                return Post(**post)
        else:
            raise PostRepositoryReadError(f"no such post with id '{post_id}'")

    def insert(self, post: Post):
        dict_post = asdict(post)
        dict_post["metadata"] = json.dumps(post.metadata, default=str)
        if os.path.exists(self.path):
            df = pd.read_parquet(self.path)
            if post.url not in df.url.values:
                df = pd.concat([df, pd.DataFrame([dict_post])])
            else:
                raise FeedRepositoryWriteError(
                    f"url '{post.url}' already exists in posts repository"
                )
        else:
            df = pd.DataFrame([dict_post])
        df.to_parquet(self.path)

    def exists(self, url: str) -> bool:
        if os.path.exists(self.path):
            df = pd.read_parquet(self.path)
            df = df[df["url"] == url]
            if len(df) > 0:
                return True
            else:
                return False
        else:
            return False
