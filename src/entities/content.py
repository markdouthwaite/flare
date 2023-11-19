import os
import uuid
from pgvector.sqlalchemy import Vector
from numpy import ndarray
from datetime import datetime
from typing import Dict, List, Any, Optional
from sqlmodel import SQLModel, Field
from src.common.constants import DATE_FORMAT
from sqlalchemy.sql.schema import Column
from sqlalchemy import JSON, String
from pydantic import BaseModel


EMBED_DIM = int(os.environ["FLARE_EMBED_DIM"])


class Content(SQLModel, table=True):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex, primary_key=True)
    url: str = Field(sa_column=Column("url", String, unique=True))
    title: str
    provider: Optional[str]
    content: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    metadata_: Dict[str, Any] = Field(
        default={}, sa_column=Column(JSON), alias="metadata"
    )
    tags: List[str] = Field(default=[], sa_column=Column(JSON))
    embedding: List[float] = Field(sa_column=Column(Vector(EMBED_DIM)))
    available: bool = True
    createdBy: str
    createdAt: datetime = Field(default_factory=lambda: datetime.now())
    updatedBy: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        json_encoders = {datetime: lambda v: v.strftime(DATE_FORMAT)}


class RawContent(BaseModel):
    url: str
    title: str
    provider: Optional[str]
    content: Dict[str, Any] = Field(default={})
    metadata: Dict[str, Any] = Field(default={}, alias="metadata")
    tags: List[str] = Field(default=[])

    class Config:
        json_encoders = {datetime: lambda v: v.strftime(DATE_FORMAT)}
