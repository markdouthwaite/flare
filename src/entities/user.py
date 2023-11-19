import uuid
from typing import Optional
from sqlalchemy import String
from sqlalchemy.sql.schema import Column
from datetime import datetime
from sqlmodel import SQLModel, Field
from src.common.constants import DATE_FORMAT


class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex, primary_key=True)
    name: str = Field(sa_column=Column("name", String, unique=True))
    slug: str = Field(sa_column=Column("slug", String, unique=True))
    email: str
    createdAt: datetime = Field(default_factory=lambda: datetime.now())
    updatedAt: Optional[datetime] = None

    class Config:
        json_encoders = {datetime: lambda v: v.strftime(DATE_FORMAT)}
