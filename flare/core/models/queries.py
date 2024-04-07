from typing import Any, List

from pydantic import BaseModel


class QueryFilter(BaseModel):
    field: str
    operator: str
    value: Any


class QueryFilterSet(BaseModel):
    filters: List[QueryFilter] = []


class QueryOrderBy(BaseModel):
    field: str
    direction: str = "desc"
