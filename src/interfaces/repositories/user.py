from typing import Protocol
from src.entities.user import User


class UserRepository(Protocol):
    def get(self, user_id: str) -> User:
        pass

    def list(self):
        pass

    def create(self, user: User):
        pass

    def delete(self, user_id: str):
        pass
