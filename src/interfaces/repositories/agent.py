from typing import Protocol
from src.entities.agent import Agent


class AgentRepository(Protocol):
    def get(self, agent_id: str) -> Agent:
        pass

    def list(self):
        pass

    def create(self, agent: Agent):
        pass

    def update(self):
        pass

    def delete(self, agent_id: str):
        pass
