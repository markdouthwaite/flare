import os
import json
from typing import Optional, Iterable
from src.entities import Post, Condition
from src.common.errors import PostReposistoryReadError
import pandas as pd
from dataclasses import asdict


class ParquetPostRepository:
    def __init__(self, path: str, primary_key: str):
        self.path = path
        self.primary_key = primary_key

    def list(
        self,
        order_by: str = None,
        descending: str = True,
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

    def get(self, post_id: str):
        if os.path.exists(self.path):
            df = pd.read_parquet(self.path)
            df = df[df["id"] == post_id]
            _posts = df.to_dict(orient="records")
            if len(_posts) < 1:
                raise PostReposistoryReadError(f"no such post with id '{post_id}'")
            else:
                # check for multiple posts?
                post = _posts[0]
                post["metadata"] = json.loads(post["metadata"])
                return Post(**post)
        else:
            posts = []
        return posts

    def insert(self, post: Post):
        dict_post = asdict(post)
        dict_post["metadata"] = json.dumps(post.metadata, default=str)
        if os.path.exists(self.path):
            df = pd.read_parquet(self.path)
            if post.url not in df.url.values:
                df = pd.concat([df, pd.DataFrame([dict_post])])
            else:
                raise PostReposistoryReadError(
                    f"url '{post.url}' already exists in posts repository"
                )
        else:
            df = pd.DataFrame([dict_post])
        df.to_parquet(self.path)
