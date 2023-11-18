from typing import List
from src.interfaces.content import ContentRepository
from dataclasses import dataclass


@dataclass
class Job:
    name: str
    callable: str
    parameters: str


@dataclass
class FeedConfig:
    id: str
    name: str
    repository: ContentRepository
    jobs: List[Job]
    created_at: str
