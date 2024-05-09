from typing import Callable, List

from pydantic import BaseModel

from .links import ExtractedLink, Link

LinkFilter = Callable[[Link], bool]
ExtractedLinkFilter = Callable[[ExtractedLink], bool]


class LinkFilterSet(BaseModel):
    filters: List[LinkFilter] = []


class ExtractedLinkFilterSet(BaseModel):
    filters: List[ExtractedLinkFilter] = []
