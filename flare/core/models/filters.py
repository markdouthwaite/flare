from typing import Iterable, Callable
from pydantic import BaseModel

from .links import Link, UnfurledLink


LinkFilter = Callable[[Link], bool]
ExtractedLinkFilter = Callable[[UnfurledLink], bool]


class LinkFilterSet(BaseModel):
    filters: Iterable[LinkFilter]


class ExtractedLinkFilterSet(BaseModel):
    filters: Iterable[ExtractedLinkFilter]
