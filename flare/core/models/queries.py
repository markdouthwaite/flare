from pydantic import BaseModel
from typing import List


class QueryFilter(BaseModel):
    field: str
    operator: str
    value: str


class QueryFilterSet(BaseModel):
    filters: List[QueryFilter] = []


class QueryOrderBy(BaseModel):
    field: str
    direction: str = "desc"
