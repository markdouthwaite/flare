from src.entities.agent import Agent
from sqlmodel import create_engine, Session, SQLModel, select


class PostgresAgentRepository:
    def __init__(self, database: str):
        self.engine = create_engine(database)
        SQLModel.metadata.create_all(self.engine)

    def create(self, agent: Agent):
        with Session(self.engine) as session:
            session.add(agent)
            session.commit()

    def get(self, agent_id: str):
        with Session(self.engine) as session:
            statement = select(Agent).where(Agent.id == agent_id)
            results = session.exec(statement)
            user = results.one()

        return user

    def list(self):
        with Session(self.engine) as session:
            statement = select(Agent)
            results = session.exec(statement)
            users = results.fetchall()
        return users

    def delete(self, agent_id: str):
        with Session(self.engine) as session:
            statement = select(Agent).where(Agent.id == agent_id)
            results = session.exec(statement)
            user = results.one()
            session.delete(user)
            session.commit()
