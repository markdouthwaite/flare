import os
import json
from src.entities import Post
import pandas as pd
from dataclasses import asdict


class ParquetPostRepository:
    def __init__(self, path: str, primary_key: str):
        self.path = path
        self.primary_key = primary_key

    def list(self):
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

    def insert(self, post: Post):
        dict_post = asdict(post)
        dict_post["metadata"] = json.dumps(post.metadata, default=str)
        if os.path.exists(self.path):
            df = pd.read_parquet(self.path)
            if post.url not in df.url.values:
                df = pd.concat([df, pd.DataFrame([dict_post])])
            else:
                raise ValueError(f"url '{post.url}' already exists in posts repository")
        else:
            df = pd.DataFrame([dict_post])
        df.to_parquet(self.path)
