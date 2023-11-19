from typing import List
from src.entities.user import User
from src.interfaces.repositories.user import UserRepository


def create_user(repository: UserRepository, name: str, slug: str, email: str) -> str:
    user = User(name=name, slug=slug, email=email)
    user_id = user.id
    repository.create(user)
    return user_id


def get_user(repository: UserRepository, user_id: str) -> User:
    return repository.get(user_id)


def list_users(repository: UserRepository) -> List[User]:
    return repository.list()


def delete_user(repository: UserRepository, user_id: str):
    repository.delete(user_id)
