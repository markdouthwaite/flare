from typing import Optional
from src.entities.content import Content
from sqlmodel import create_engine, Session, SQLModel, select
from src.common.embeddings import embed_document


class PostgresContentRepository:
    def __init__(self, database: str):
        self.engine = create_engine(database)
        SQLModel.metadata.create_all(self.engine)

    def insert(self, content: Content):
        with Session(self.engine) as session:
            session.add(content)
            session.commit()

    def get(self, content_id: str):
        with Session(self.engine) as session:
            statement = select(Content).where(Content.id == content_id)
            results = session.exec(statement)
            return results.one()

    def search(
        self, query_text: str, limit: int = 5, provider: Optional[str] = None, **kwargs
    ):
        embedding = embed_document(query_text, **kwargs)
        with Session(self.engine) as session:
            statement = select(Content).where(Content.available == True)

            if provider is not None:
                statement = statement.where(Content.provider == provider)

            statement = statement.order_by(
                Content.embedding.l2_distance(embedding)
            ).limit(limit)
            print(statement)
            results = session.exec(statement)
            return results.fetchall()

    def similar(self, content_id: str, limit: int = 5):
        target = self.get(content_id)
        embedding = target.embedding
        with Session(self.engine) as session:
            results = session.exec(
                select(Content)
                .order_by(Content.embedding.l2_distance(embedding))
                .limit(limit)
            )
            return results.fetchall()
