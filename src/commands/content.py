from typing import Any, List, Optional

import sqlalchemy.exc

from src.common.embeddings import embed_document
from src.entities.user import User
from src.entities.content import Content, RawContent
from src.interfaces.repositories.content import ContentRepository, RawContentRepository
from src.common import urls


def ingest_content(
    user: User,
    repository: ContentRepository,
    url: str,
    embedding_model: str,
    **kwargs: Any,
) -> str:
    raw_content = urls.unfurl(url, **kwargs)
    return insert_content(user, repository, raw_content, embedding_model)


def insert_content(
    user: User,
    repository: ContentRepository,
    raw_content: RawContent,
    embedding_model: str,
) -> str:
    body = raw_content.content.get("body")
    embedding = embed_document(body, model_name=embedding_model).tolist()
    content = Content(**raw_content.dict(), embedding=embedding, createdBy=user.id)
    content_id = content.id
    repository.insert(content)
    return content_id


def batch_insert_content(
    user: User,
    raw_content_repository: RawContentRepository,
    content_repository: ContentRepository,
    sample: Optional[float] = None,
    **kwargs,
):
    for raw_content in raw_content_repository.iter(sample=sample):
        print("inserting:", raw_content.url)
        try:
            insert_content(user, content_repository, raw_content, **kwargs)
        except sqlalchemy.exc.StatementError:
            print(f"failed to insert record for '{raw_content.url}'")


def get_content(repository: ContentRepository, content_id: str):
    return repository.get(content_id)


def list_content(repository: ContentRepository) -> List[Content]:
    return repository.list()


def search_content(
    repository: ContentRepository, query_text: str, limit: int = 10, **kwargs
) -> List[Content]:
    return repository.search(query_text=query_text, limit=limit, **kwargs)


def similar_content(repository: ContentRepository, content_id: str, limit: int = 10):
    return repository.similar(content_id, limit=limit)
