from pandas import read_gbq
from .adapters import to_indexed_item


class BigQueryIndexedItemRepository:
    def __init__(
        self,
        schema: str,
        table: str,
        project: str,
        start_date: str,
        end_date: str,
        max_rows: int = 10000,
        **kwargs,
    ):
        self.schema = schema
        self.table = table
        self.project = project
        self.max_rows = max_rows
        self.start_date = start_date
        self.end_date = end_date
        super().__init__(**kwargs)

    def get(self):
        df = read_gbq(
            f"SELECT * FROM `{self.project}.{self.schema}.{self.table}` "
            f"WHERE load_date >= '{self.start_date}' "
            f"AND load_date <= '{self.end_date}' "
            f"LIMIT {self.max_rows};",
            project_id=self.project,
        )
        print(len(df), "loaded")
        return (to_indexed_item(s) for s in df.to_dict(orient="records"))
