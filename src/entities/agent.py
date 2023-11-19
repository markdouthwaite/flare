import uuid
from datetime import datetime
from typing import List
from sqlmodel import SQLModel, Field, Column, String, ARRAY


class Agent(SQLModel, table=True):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex, primary_key=True)
    name: str
    slug: str = Field(sa_column=Column("slug", String, unique=True))
    createdBy: str = Field(foreign_key="user.slug")
    createdAt: datetime = Field(default_factory=lambda: datetime.now())
    hooks: List[str] = Field(default=[], sa_column=Column(ARRAY(String)))
