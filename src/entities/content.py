from typing import Optional, List
from src.entities.tag import Tag
from dataclasses import dataclass


@dataclass
class RawContent:
    url: str
    title: str
    body: str
    tags: List[Tag]
    featured: bool = False
    visibility: str = "public"  # enum
    og_image: Optional[str] = None
    og_title: Optional[str] = None
    og_description: Optional[str] = None


@dataclass
class Content:
    id: str
    url: str
    title: str
    body: str
    created_at: str
    tags: List[Tag]
    summary: Optional[str] = None
    read_time: Optional[int] = None
    score: Optional[int] = None
    og_image: Optional[str] = None
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    featured: bool = False
    visibility: str = "public"  # enum
    updated_at: Optional[str] = None
    published_at: Optional[str] = None
