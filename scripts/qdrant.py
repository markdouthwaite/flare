from src.commands.user import get_user
from src.commands.content import (
    ingest_content,
    list_content,
    get_content,
    search_content,
)
from src.infrastructure.repositories.sqlite import (
    SQLiteUserRepository,
    SQLiteContentRepository,
)
from src.infrastructure.repositories.qdrant import QdrantContentRepository

user_repo = SQLiteUserRepository(database="sqlite:///flare.db")
content_repo = QdrantContentRepository(database=".flare.content.db")

user = get_user(user_repo, "f8965a7251a84403a445d0f15f824a46")

urls = [
    "https://blog.research.google/2023/11/responsible-ai-at-google-research_16.html",
    "https://blog.research.google/2023/11/enabling-large-scale-health-studies-for.html",
    "https://mark.douthwaite.io/7-reasons-to-work-at-a-startup-and-1-reason-not-to/",
    "https://mark.douthwaite.io/intro-to-software-testing-load-testing-an-api/",
    "https://ai.meta.com/llama/",
    "https://github.com/markdouthwaite/xanthus",
]

# for url in urls:
#     print(url)
#     ingest_content(content_repo, user, url)


# # ingest_content(content_repo, user, "https://mark.douthwaite.io/about")
#
# print(list_content(content_repo))
# print(get_content(content_repo, "089d047abd8e49349c337f3a278d43e9"))

for item in search_content(content_repo, "health studies at google", limit=10):
    print(item)
from src.commands.user import get_user, create_user
from src.commands.content import (
    ingest_content,
    list_content,
    get_content,
    search_content,
)
from src.infrastructure.repositories.postgres import (
    PostgresUserRepository,
    PostgresContentRepository,
)

connection_string = "postgresql://postgres:password@127.0.0.1:5432/postgres"
user_repo = PostgresUserRepository(database=connection_string)
content_repo = PostgresContentRepository(database=connection_string)

# create_user(user_repo, "Mark Douthwaite", "markdouthwaite", "mark@douthwaite.io")

user = get_user(user_repo, "601217a121f747f1b7d2ae6c03e7392f")

urls = [
    "https://blog.research.google/2023/11/responsible-ai-at-google-research_16.html",
    "https://blog.research.google/2023/11/enabling-large-scale-health-studies-for.html",
    # "https://mark.douthwaite.io/7-reasons-to-work-at-a-startup-and-1-reason-not-to/",
    # "https://mark.douthwaite.io/intro-to-software-testing-load-testing-an-api/",
    # "https://ai.meta.com/llama/",
    # "https://github.com/markdouthwaite/xanthus",
]

# for url in urls:
#     print(url)
#     ingest_content(content_repo, user, url)

search_content(content_repo, "blob")


def init_content_index(name: str = "content_index"):
    engine = create_engine(database)
    index = Index(
        name,
        Content.embedding,
        postgresql_using="hnsw",
        postgresql_with={"m": 16, "ef_construction": 64},
        postgresql_ops={"embedding": "vector_l2_ops"},
    )
    index.create(engine)


# import os
#
# import fire
# from src.commands.content import (
#     search_content as _search_content,
#     ingest_content as _ingest_content,
#     batch_insert_content as _batch_insert_content,
# )
# from src.commands.user import create_user, get_user
# from sqlalchemy import Index, create_engine
# from src.infrastructure.repositories.postgres import (
#     PostgresUserRepository,
#     PostgresContentRepository,
# )
# from src.infrastructure.repositories.parquet import ParquetRawContentRepository
# from src.entities.content import Content
#
#
# def init_admin(
#     name: str = "admin", slug: str = "admin", email: str = "mark@douthwaite.io"
# ):
#     user_id = create_user(user_repo, name=name, slug=slug, email=email)
#     print(user_id)
#
#
# def batch_insert_content(
#     user_id: str, path: str = "data/development/content.parquet", sample: float = 0.1
# ):
#     raw_content_repo = ParquetRawContentRepository(path=path)
#     user = get_user(user_repo, user_id)
#     _batch_insert_content(user, raw_content_repo, content_repo, sample=sample)
#
#
# def ingest_content(user_id: str, url: str):
#     user = get_user(user_repo, user_id)
#     _ingest_content(user, content_repo, url)
#
#
# def search_content(query_text: str, limit: int = 3):
#     for item in _search_content(content_repo, query_text, limit=limit):
#         print(item.url, item.title)
#
#
# if __name__ == "__main__":
#     fire.Fire()
