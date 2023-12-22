from typing import Iterable
from src.entities import IndexedItem
import pandas as pd
from .adapters import to_indexed_item


class ParquetIndexedItemRepository:
    def __init__(self, path: str):
        self.path = path

    def get(self) -> Iterable[IndexedItem]:
        df = pd.read_parquet(self.path)
        return (to_indexed_item(s) for s in df.to_dict(orient="records"))
