from typing import List, Optional, Dict, Any, Iterable, Callable
from dataclasses import dataclass
from datetime import datetime

import bs4


@dataclass
class Content:
    text: str
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None


@dataclass
class ExtractedItem:
    id: str
    url: str
    content: Content
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class Tag:
    name: str


@dataclass
class Post:
    id: str
    url: str
    kind: str
    title: str
    description: Optional[str]
    text: str
    image_url: Optional[str]
    locale: str
    excerpt: str
    featured: bool
    status: str
    readability: int
    read_time: int
    rating: float
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime]
    updated_by: Optional[str]
    tags: List[Tag]


Extractor = Callable[[str], ExtractedItem]
Scorer = Callable[[ExtractedItem], float]
Filter = Callable[[Post], bool]
Summarizer = Callable[[str], str]


@dataclass
class Source:
    name: str
    kind: str
    filters: Iterable[Filter]
    extractor: Extractor
    scorer: Scorer
    summarizer: Summarizer
    url_patterns: Dict[str, Any]


Sources = Dict[str, Source]

HtmlDocument = bs4.BeautifulSoup


@dataclass
class Condition:
    field_name: str
    condition: str
    value: Any
