from src.entities.user import User
from sqlmodel import create_engine, Session, SQLModel, select


class PostgresUserRepository:
    def __init__(self, database: str):
        self.engine = create_engine(database)
        SQLModel.metadata.create_all(self.engine)

    def create(self, user: User):
        with Session(self.engine) as session:
            session.add(user)
            session.commit()

    def get(self, user_id: str):
        with Session(self.engine) as session:
            statement = select(User).where(User.id == user_id)
            results = session.exec(statement)
            user = results.one()

        return user

    def list(self):
        with Session(self.engine) as session:
            statement = select(User)
            results = session.exec(statement)
            users = results.fetchall()
        return users

    def delete(self, user_id: str):
        with Session(self.engine) as session:
            statement = select(User).where(User.id == user_id)
            results = session.exec(statement)
            user = results.one()
            session.delete(user)
            session.commit()
