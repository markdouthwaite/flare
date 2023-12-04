from typing import Any, Sequence, Optional, Union
from src.entities.candidate import Candidate
from sqlmodel import create_engine, Session, SQLModel, select


class PostgresCandidateRepository:
    def __init__(self, database: str):
        self.engine = create_engine(database)
        SQLModel.metadata.create_all(self.engine)

    def insert(self, item: Candidate):
        with Session(self.engine) as session:
            session.add(item)
            session.commit()

    def update(self, item: Candidate):
        with Session(self.engine) as session:
            statement = select(Candidate).where(Candidate.id == item.id)
            db_item = session.exec(statement).one()
            db_item.score = item.score
            db_item.attributes = item.attributes
            db_item.updatedAt = item.updatedAt
            db_item.updatedBy = item.updatedBy
            db_item.featured = item.featured
            db_item.available = item.available
            db_item.publishedAt = item.publishedAt
            session.add(db_item)
            session.commit()

    def _list(
        self,
        entity: Any,
        available: bool = False,
        featured: Optional[bool] = None,
        limit: Optional[int] = None,
        order_by: Optional[Any] = None,
    ) -> Sequence[Union[Candidate, str]]:
        with Session(self.engine) as session:
            statement = select(entity)
            if limit is not None:
                statement = statement.limit(limit)
            if available:
                statement = statement.where(Candidate.available == available)
            if featured:
                statement = statement.where(Candidate.featured == featured)
            if order_by is not None:
                statement = statement.order_by(order_by)

            results = session.exec(statement)
            items = results.fetchall()
        return items

    def list(self, *args, **kwargs):
        return self._list(Candidate, *args, **kwargs)

    def list_ids(self, *args, **kwargs) -> Sequence[str]:
        return self._list(Candidate.id, *args, **kwargs)

    def list_content_ids(self, *args, **kwargs) -> Sequence[str]:
        return self._list(Candidate.content_id, *args, **kwargs)
