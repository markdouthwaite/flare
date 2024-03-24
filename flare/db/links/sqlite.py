from flare.core.models.links import RichLink
from flare.core.errors import RichLinkRepositoryReadError, RichLinkRepositoryWriteError

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    MetaData,
    String,
    Table,
    create_engine,
    select,
)
from sqlalchemy.exc import OperationalError, IntegrityError


_links = Table(
    "rich_links",
    MetaData(),
    Column("id", String),
    Column("url", String, primary_key=True),
    Column("title", String),
    Column("description", String, nullable=True),
    Column("image", JSON, nullable=True),
    Column("metadata", JSON, nullable=True),
    Column("locale", String),
    Column("excerpt", String),
    Column("read_time", Float),
    Column("readability", Float),
    Column("tags", JSON),
    Column("attributes", JSON, nullable=True),
    Column("featured", Boolean),
    Column("available", String),
    Column("index_date", String),
    Column("created_at", DateTime),
    Column("updated_at", DateTime, nullable=True),
)


class SQLRichLinkRepository:
    def __init__(self, path: str):
        self.path = path
        self.engine = create_engine(path)
        self._maybe_create()

    def _maybe_create(self):
        try:
            _links.create(self.engine)
        except OperationalError:
            print("table already exists")

    def get(self, rich_link_id: str) -> RichLink:
        statement = select(_links).where(_links.c.id == rich_link_id)

        with self.engine.connect() as conn:
            res = conn.execute(statement)
            rich_link_record = res.fetchone()

            if rich_link_record is None:
                raise RichLinkRepositoryReadError(
                    f"no such rich link with id '{rich_link_id}'"
                )
        print(rich_link_record)
        return RichLink(**dict(zip(RichLink.__fields__, rich_link_record)))

    def insert(self, rich_link: RichLink):
        rich_link_dict = rich_link.dict()
        print(rich_link_dict)
        statement = _links.insert().values(**rich_link_dict)
        try:
            with self.engine.connect() as conn:
                conn.execute(statement)
                conn.commit()
        except IntegrityError as err:
            raise RichLinkRepositoryWriteError(
                f"url '{rich_link.url}' already exists in rich link repository"
            ) from err
