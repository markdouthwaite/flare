import datetime
import uuid
from typing import List
from src.entities.content import RawContent, Content
from src.entities.feed import FeedConfig


DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


# feed
def create_content(raw_content: RawContent, feed_config: FeedConfig):
    content = Content(
        id=uuid.uuid4().hex,
        url=raw_content.url,
        title=raw_content.title,
        body=raw_content.body,
        summary=None,
        featured=False,
        visibility="private",
        read_time=None,
        og_image=raw_content.og_image,
        og_title=raw_content.og_title,
        og_description=raw_content.og_description,
        created_at=datetime.datetime().now().strftime(DATE_FORMAT),
        updated_at=None,
        published_at=None
    )
    feed_config.repository.create(content)


def list_content(feed_config: FeedConfig) -> List[Content]:
    return feed_config.repository.list()


def trigger_job(feed_config: FeedConfig, job_id: str):
    pass
