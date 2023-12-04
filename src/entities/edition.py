from datetime import datetime
from typing import Optional, Dict, List, Any
from pydantic import BaseModel


class Item(BaseModel):
    id: str
    url: str
    title: str
    summary: str
    image_url: Optional[str] = None
    score: float
    featured: bool
    published_at: datetime
    metadata: Dict[str, Any]


class Section(BaseModel):
    featured: List[Item]
    items: List[Item]


class Edition(BaseModel):
    sections: Dict[str, Section]
    timestamp: float
