from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

from src.interfaces import PostRepository

from . import Post


@dataclass
class Section:
    name: str
    posts: List[Post]


@dataclass
class Feed:
    name: str
    sections: List[Section]
    updated_by: str
    updated_at: datetime


FeedBuilder = Callable[[str, Tuple[Any, ...], Dict[Any, Any], PostRepository], Feed]


@dataclass
class FeedBuildConfig:
    builder: FeedBuilder
    args: Optional[Tuple[Any, ...]] = ()
    kwargs: Optional[Dict[Any, Any]] = field(default_factory=lambda: {})


FeedIndex = Dict[str, FeedBuildConfig]
