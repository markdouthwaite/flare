import os

import typer
from typing import Optional
import src.commands as cmd
from src.common import backends
from sqlalchemy import Index, create_engine
from src.entities.content import Content
from src.common.backends import postgres_connection_string
from src.infrastructure.repositories.parquet import ParquetRawContentRepository

EMBED_MODEL = os.environ["FLARE_EMBED_MODEL"]
BACKEND = os.environ.get("FLARE_BACKEND", "default")

app = typer.Typer()
user_repo, content_repo, _ = backends.initialize(BACKEND)


@app.command()
def ingest(user_id: str, url: str):
    user = cmd.user.get_user(user_repo, user_id)
    cmd.content.ingest_content(user, content_repo, url, embedding_model=EMBED_MODEL)


@app.command()
def batch_insert(
    user_id: str,
    path: str = "data/development/content.parquet",
    sample: Optional[float] = None,
):
    raw_content_repo = ParquetRawContentRepository(path=path)
    user = cmd.user.get_user(user_repo, user_id)
    cmd.content.batch_insert_content(
        user, raw_content_repo, content_repo, sample=sample
    )


@app.command()
def get(content_id: str):
    content = cmd.content.get_content(content_repo, content_id)
    print(content.dict())


@app.command()
def search(query_text: str, limit: int = 10, provider: Optional[str] = None):
    for content in cmd.content.search_content(
        content_repo, query_text, limit=limit, provider=provider
    ):
        print(content.id, content.title, content.url)


@app.command()
def similar(content_id: str, limit: int = 10):
    for content in cmd.content.similar_content(content_repo, content_id, limit=limit):
        print(content.id, content.title, content.url)


@app.command()
def init_index(name: str):
    database = postgres_connection_string()
    engine = create_engine(database)
    index = Index(
        name,
        Content.embedding,
        postgresql_using="hnsw",
        postgresql_with={"m": 16, "ef_construction": 64},
        postgresql_ops={"embedding": "vector_l2_ops"},
    )
    index.create(engine)
