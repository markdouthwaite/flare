import os
import json
from typing import Iterable
from src.entities import Post
import pandas as pd
from dataclasses import asdict
from itertools import islice
from src.common.scoring import decay
from datetime import datetime


def delta(d):
    td = datetime.now() - d
    return int(td.days)


class ParquetPostRepository:
    def __init__(self, path: str):
        self.path = path

    def page(self):
        if os.path.exists(self.path):
            df = pd.read_parquet(self.path)
            posts = [Post(**_) for _ in df.to_dict(orient="records")]
            posts = [_ for _ in posts if _.status == "published"]
        else:
            posts = []

        articles = (post for post in posts if post.kind not in ["code", "papers"])
        papers = (post for post in posts if post.kind == "papers")
        repos = (post for post in posts if post.kind == "code")

        top_articles = islice(
            sorted(
                articles, key=lambda _: -decay(_.relevance, delta(_.created_at), 21)
            ),
            6,
        )

        top_papers = islice(
            sorted(papers, key=lambda _: -decay(_.relevance, delta(_.created_at), 21)),
            6,
        )

        top_repos = islice(
            sorted(repos, key=lambda _: -decay(_.relevance, delta(_.created_at), 21)), 6
        )

        return [*list(top_articles), *list(top_papers), *list(top_repos)]

    def get(self) -> Iterable[Post]:
        if os.path.exists(self.path):
            df = pd.read_parquet(self.path)
            posts = (Post(**_) for _ in df.to_dict(orient="records"))
        else:
            posts = ()
        return posts

    def insert(self, post: Post):
        dict_post = asdict(post)
        dict_post["metadata"] = json.dumps(post.metadata, default=str)
        if os.path.exists(self.path):
            df = pd.read_parquet(self.path)
            df = pd.concat([df, pd.DataFrame([dict_post])])
        else:
            df = pd.DataFrame([dict_post])
        df.to_parquet(self.path)

    def insert_many(self, posts: Iterable[Post]):
        if os.path.exists(self.path):
            df = pd.read_parquet(self.path)
            df = pd.concat([df, pd.DataFrame([asdict(post) for post in posts])])
        else:
            df = pd.DataFrame([asdict(post) for post in posts])
        df.to_parquet(self.path)
