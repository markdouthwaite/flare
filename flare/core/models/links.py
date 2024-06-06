from datetime import datetime
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Protocol,
    Tuple,
)

from numpy import ndarray
from pydantic import BaseModel, Field, field_serializer

from flare.core.identifiers import generate_id

LinkMetadata = Dict[str, Any]
EmbeddingModel = Callable[[str], ndarray]


class UnfurledBody(BaseModel):
    title: str
    description: Optional[str]
    image_url: Optional[str]
    body: str


class Link(BaseModel):
    id: str = Field(default_factory=generate_id)
    url: str


class LinkText(BaseModel):
    type: str = "text/plain"
    value: str


class LinkImage(BaseModel):
    url: str


class ExtractedLink(BaseModel):
    id: str
    url: str
    title: Optional[str]
    description: Optional[str]
    text: LinkText
    image: Optional[LinkImage]
    metadata: Optional[LinkMetadata]
    tags: List[str] = Field(default_factory=lambda: [])


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
    image: Optional[LinkImage]
    metadata: Optional[LinkMetadata]
    locale: str
    excerpt: str
    read_time: float
    readability: float
    tags: List[str]
    attributes: RichLinkAttributes
    featured: bool = False
    available: bool = True
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        arbitrary_types_allowed = True

    @field_serializer('created_at')
    def serialize_created_at(self, created_at: datetime, _info):
        return created_at.strftime("%Y-%m-%d %H:%M:%S.%f")


class RichLinkConfig(BaseModel):
    summarizer: ExtractedLinkSummarizer
    attribute_scorers: List[RichLinkAttributeScorer]
    embedding_model: EmbeddingModel


class FeedItem(RichLink):
    rank: int
    featured: bool = False


class RichLinkSet(BaseModel):
    links: List[RichLink]


class RichLinkRepository(Protocol):
    def get(self, rich_link_id: str) -> RichLink:
        pass

    def insert(self, rich_link: RichLink):
        pass

    def list(self) -> RichLinkSet:
        pass

    def exists(self, rich_link_url: str) -> bool:
        pass


class RichLinkPostprocessor(Protocol):
    def __call__(self, rich_link: RichLink) -> RichLink:
        pass
