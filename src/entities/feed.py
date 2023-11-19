import uuid
from typing import Dict, Any, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, String


class FeedContent(SQLModel, table=True):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex, primary_key=True)
    content_id: str
    scores: Dict[str, float]
    available: bool = False
    featured: bool = False
    expiresAt: Optional[datetime] = None
    publishedAt: Optional[datetime] = None
    addedAt: datetime = Field(default_factory=lambda: datetime.now())
    addedBy: str = Field(foreign_key="agent.slug")
    addedTo: str
