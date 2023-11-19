import os
from src.infrastructure.repositories.postgres import (
    PostgresUserRepository,
    PostgresContentRepository,
    PostgresAgentRepository,
)


def postgres_connection_string():
    username = os.environ["FLARE_POSTGRES_USERNAME"]
    password = os.environ["FLARE_POSTGRES_PASSWORD"]
    host = os.environ["FLARE_POSTGRES_HOST"]
    port = os.environ["FLARE_POSTGRES_PORT"]
    db = os.environ["FLARE_POSTGRES_DB"]
    database = f"postgresql://{username}:{password}@{host}:{port}/{db}"
    return database


def initialize(name: str = "default"):
    match name:
        case "default":
            database = postgres_connection_string()
            user_repo = PostgresUserRepository(database)
            content_repo = PostgresContentRepository(database)
            agent_repo = PostgresAgentRepository(database)
        case _:
            raise ValueError(f"unsupported backend option '{name}'")

    return user_repo, content_repo, agent_repo
