from datetime import datetime
from typing import Any, Dict, Tuple

from src.entities.feeds import Feed, Section
from src.interfaces import PostRepository


def firehose(
    name: str, args: Tuple[Any, ...], kwargs: Dict[Any, Any], post_repo: PostRepository
) -> Feed:
    return Feed(
        name=name,
        sections=[Section(name="main", posts=list(post_repo.list()))],
        updated_by="system",
        updated_at=datetime.now(),
    )
