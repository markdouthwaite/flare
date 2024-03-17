from typing import Callable, Iterable

from pydantic import BaseModel

from .links import Link, ExtractedLink

LinkFilter = Callable[[Link], bool]
ExtractedLinkFilter = Callable[[ExtractedLink], bool]


class LinkFilterSet(BaseModel):
    filters: Iterable[LinkFilter]


class ExtractedLinkFilterSet(BaseModel):
    filters: Iterable[ExtractedLinkFilter]
