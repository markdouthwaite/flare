from datetime import datetime
from typing import Any, Dict, Tuple

from flare.entities.feeds import Feed, Section
from flare.interfaces import PostRepository


def firehose(
    name: str, _: Tuple[Any, ...], __: Dict[Any, Any], post_repo: PostRepository
) -> Feed:
    return Feed(
        name=name,
        sections=[Section(name="main", posts=list(post_repo.list()))],
        updated_by="system",
        updated_at=datetime.now(),
    )
