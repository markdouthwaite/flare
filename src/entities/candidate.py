import uuid
from typing import Dict, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, JSON


class Candidate(SQLModel, table=True):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex, primary_key=True)
    content_id: str
    type: str
    score: Optional[float] = None
    attributes: Dict[str, float] = Field(sa_column=Column(JSON))
    available: bool = False
    featured: bool = False
    publishedAt: Optional[datetime] = None
    addedAt: datetime = Field(default_factory=lambda: datetime.now())
    addedBy: str = Field(foreign_key="agent.slug")
    updatedAt: Optional[datetime] = None
    updatedBy: Optional[str] = Field(foreign_key="agent.slug")
