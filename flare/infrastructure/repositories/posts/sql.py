from dataclasses import asdict
from typing import Iterable, Optional

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    select,
)
from sqlalchemy.exc import IntegrityError, OperationalError

from flare.common.errors import PostRepositoryReadError, PostRepositoryWriteError
from flare.entities import Condition, Post

_posts = Table(
    "post",
    MetaData(),
    Column("id", String),
    Column("url", String, primary_key=True),
    Column("kind", String),
    Column("title", String),
    Column("description", String, nullable=True),
    Column("text", String),
    Column("image_url", String, nullable=True),
    Column("locale", String),
    Column("excerpt", String),
    Column("featured", Boolean),
    Column("status", String),
    Column("readability", Integer),
    Column("read_time", Integer),
    Column("rating", Float),
    Column("metadata", JSON, nullable=True),
    Column("created_at", DateTime),
    Column("created_by", String),
    Column("updated_at", DateTime, nullable=True),
    Column("updated_by", String, nullable=True),
    Column("tags", JSON),
)


class SQLPostRepository:
    def __init__(self, path: str):
        self.path = path
        self.engine = create_engine(path)
        self._maybe_create()

    def _maybe_create(self):
        try:
            _posts.create(self.engine)
        except OperationalError:
            print("table already exists")

    def list(
        self,
        order_by: Optional[str] = None,
        where: Optional[Iterable[Condition]] = None,
        limit: Optional[int] = None,
        descending: bool = False,
        featured: bool = False,
        kind: Optional[str] = None,
    ):
        statement = select(_posts)

        if order_by is not None:
            order_by_column = getattr(_posts.c, order_by)
            if descending:
                order_by_column = order_by_column.desc()
            statement = statement.order_by(order_by_column)

        if featured:
            statement = statement.where(_posts.c.featured.is_(True))

        if kind is not None:
            statement = statement.where(_posts.c.kind.is_(kind))

        if where is not None:
            for condition in where:
                if condition.operator == "equals":
                    statement = statement.where(
                        getattr(_posts.c, condition.field_name) == condition.value
                    )
                else:
                    raise PostRepositoryReadError(
                        f"unknown operator in condition '{condition.operator}'."
                    )

        if limit is not None:
            statement = statement.limit(limit)

        with self.engine.connect() as conn:
            res = conn.execute(statement)
            return [Post(*p) for p in res.fetchall()]

    def get(self, post_id: str) -> Post:
        statement = select(_posts).where(_posts.c.id == post_id)

        with self.engine.connect() as conn:
            res = conn.execute(statement)
            post_record = res.fetchone()

            if post_record is None:
                raise PostRepositoryReadError(f"no such post with id '{post_id}'")

        return Post(*post_record)

    def insert(self, post: Post):
        dict_post = asdict(post)
        statement = _posts.insert().values(**dict_post)
        try:
            with self.engine.connect() as conn:
                conn.execute(statement)
                conn.commit()
        except IntegrityError as err:
            raise PostRepositoryWriteError(
                f"url '{post.url}' already exists in posts repository"
            ) from err

    def exists(self, url: str) -> bool:
        statement = select(_posts).where(_posts.c.url == url)

        with self.engine.connect() as conn:
            res = conn.execute(statement)
            post_record = res.fetchone()

        return post_record is not None
