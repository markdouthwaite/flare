import pandas as pd
from typing import Callable, Optional, Iterable
from src.entities.content import RawContent
from src.common.normalize import normalize_legacy_record


class ParquetRawContentRepository:
    def __init__(
        self,
        path: str,
        adapter: Callable[[pd.Series], RawContent] = normalize_legacy_record,
    ):
        self.df = pd.read_parquet(path)
        self.adapter = adapter

    def iter(self, sample: Optional[float] = None) -> Iterable[RawContent]:
        if sample is not None:
            df = self.df.sample(frac=sample)
        else:
            df = self.df
        return (_ for _ in df.apply(self.adapter, axis=1) if _ is not None)
