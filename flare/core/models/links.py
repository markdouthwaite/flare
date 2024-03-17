from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple, Protocol

from pydantic import BaseModel

from .tags import Tag

LinkMetadata = Dict[str, Any]


class UnfurledBody(BaseModel):
    title: str
    description: Optional[str]
    image_url: Optional[str]
    body: str


class Link(BaseModel):
    url: str


class LinkText(BaseModel):
    type: str = "text/plain"
    value: str


class LinkImage(BaseModel):
    url: str


class ExtractedLink(BaseModel):
    url: str
    title: Optional[str]
    description: Optional[str]
    text: LinkText
    image: Optional[LinkImage]
    metadata: Optional[LinkMetadata]
    tags: List[Tag]


LinkExtractorConfig = Dict[str, Any]


LinkExtractor = Callable[[Link, LinkExtractorConfig], ExtractedLink]
ExtractedLinkSummarizer = Callable[[str], str]


RichLinkAttributes = Dict[str, float]


RichLinkAttributeScorer = Callable[[ExtractedLink], Tuple[str, float]]


class RichLink(BaseModel):
    id: str
    url: str
    title: Optional[str]
    description: Optional[str]
    text: LinkText
    image: Optional[LinkImage]
    metadata: Optional[LinkMetadata]
    locale: str
    excerpt: str
    read_time: float
    readability: float
    tags: List[Tag]
    attributes: RichLinkAttributes
    featured: bool = False
    available: bool = True
    created_at: datetime
    updated_at: Optional[datetime]


class RichLinkConfig(BaseModel):
    summarizer: ExtractedLinkSummarizer
    attribute_scorers: List[RichLinkAttributeScorer]


class FeedItem(RichLink):
    rank: int
    featured: bool = False


class RichLinkRepository(Protocol):
    def get(self, rich_link_id: str) -> RichLink:
        pass

    def insert(self, rich_link: RichLink):
        pass

    def list(self):
        pass

    def exists(self, rich_link_url: str) -> bool:
        pass
