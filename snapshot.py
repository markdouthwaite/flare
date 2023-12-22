import json
from datetime import datetime
from src.entities import IndexedItem, Post, Tag
from src.common.identifier import generate_id
from src.common.keywords import MACHINE_LEARNING
from src.common.text import readability, read_time, summarize
from src.common.validators import (
    validate_locale,
    validate_domain,
    validate_keywords,
    validate_content_text_length,
    validate_github_repo_language,
    validate_is_active_github_repo,
    validate_unique_url,
    validate_title,
    validate_github_origin,
    validate_awesome_lists,
    validate_arxiv_origin,
    validate_github_repo_popularity,
)
from src.common.scoring import featured, relevance, status
from src.infrastructure.repositories.indexed_item.parquet import (
    ParquetIndexedItemRepository,
)
from src.infrastructure.repositories.post.parquet import ParquetPostRepository
from src.infrastructure.repositories.indexed_item.bigquery import (
    BigQueryIndexedItemRepository,
)
from dataclasses import asdict


# indexed_items_repo = ParquetIndexedItemRepository(
#     path="data/development/indexed_item.parquet"
# )

indexed_items_repo = BigQueryIndexedItemRepository(
    schema="transform",
    table="resource",
    project="vigil-344111",
    start_date="2023-12-19",
    end_date="2023-12-20",
)

posts_repo = ParquetPostRepository(path="data/development/post.parquet")


EXCLUDED_DOMAINS = {"youtube.com", "twitter.com", "nytimes.com"}


EXISTING_URLS = {_.url for _ in posts_repo.get()}


def filtered(item: IndexedItem) -> bool:
    filters = [
        (validate_locale, {"en", "en-US", "en-GB"}),
        (validate_domain, EXCLUDED_DOMAINS),
        (validate_content_text_length, 250),
        (validate_keywords, MACHINE_LEARNING, 2),
        (validate_github_repo_language, {"Python"}),
        (validate_is_active_github_repo, 90),
        (validate_github_repo_popularity, 25),
        (validate_unique_url, EXISTING_URLS),
        (validate_title,),
        (validate_github_origin,),
        (validate_awesome_lists,),
        (validate_arxiv_origin,),
    ]

    for f, *args in filters:
        if not f(item, *args):
            return False

    return True


def source_to_kind(s):
    match s:
        case "github":
            return "code"
        case "hacker_news":
            return "article"
        case "arxiv":
            return "paper"
        case _:
            return "miscellaneous"


def process(item: IndexedItem) -> Post:
    post = Post(
        id=generate_id(),
        url=item.url,
        kind=source_to_kind(item.source),
        title=item.content.title,
        image_url=item.content.image_url,
        locale=item.locale,
        excerpt=summarize(item.content.text),
        featured=False,
        status="unpublished",
        readability=readability(item.content.text),
        read_time=read_time(item.content.text),
        relevance=relevance(item),
        created_at=datetime.now(),
        created_by="default",
        updated_at=None,
        updated_by=None,
        tags=[Tag(name=source_to_kind(item.source))],
    )

    post.featured = featured(post)
    post.status = status(post)
    return post


items = list(indexed_items_repo.get())
valid_items = [_ for _ in items if filtered(_)]
posts = [process(_) for _ in valid_items]

# take top x items with most hits
print(len(valid_items), len(items))

posts_repo.insert_many(posts)

with open("page-new.json", "w") as page:
    data = {"posts": [asdict(_) for _ in posts_repo.page()]}
    json.dump(data, page, indent=4, default=lambda _: str(_))
