from src.entities import ExtractedItem, Post, Source, Tag
from src.common.identifier import generate_id
from src.common import locale
from src.common.extract.metadata import get_read_time, get_readability
from datetime import datetime


def to_post(item: ExtractedItem, source: Source) -> Post:
    post = Post(
        id=generate_id(),
        url=item.url,
        kind=source.kind,
        title=item.content.title,
        description=item.content.description,
        image_url=item.content.image_url,
        text=item.content.text,
        excerpt=source.summarizer(item.content.text),
        locale=locale.detect(item.content.text),
        featured=False,
        status="unpublished",
        read_time=get_read_time(item.content.text),
        readability=get_readability(item.content.text),
        rating=source.scorer(item),
        metadata=item.metadata,
        created_at=datetime.now(),
        created_by="system",
        updated_at=None,
        updated_by=None,
        tags=[Tag(name=source.kind)],
    )
    return post
