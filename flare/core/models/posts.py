from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel
from .tags import Tag

PostMetadata: Dict[str, Any]


class Post(BaseModel):
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
    metadata: Optional[PostMetadata]
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime]
    updated_by: Optional[str]
    tags: List[Tag]
