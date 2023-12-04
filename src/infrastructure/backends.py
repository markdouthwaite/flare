import os
from dataclasses import dataclass
from src.interfaces import scorers, summarizers
from src.interfaces.repositories import candidate, agent, content, user
from src.infrastructure.repositories.postgres import (
    PostgresUserRepository,
    PostgresContentRepository,
    PostgresAgentRepository,
    PostgresCandidateRepository,
)
from src.infrastructure.scorers.openai import OpenAIScorer
from src.infrastructure.summarizers.openai import OpenAISummarizer
from src.infrastructure.summarizers.identity import IdentitySummarizer


@dataclass
class Backend:
    agents: agent.AgentRepository
    users: user.UserRepository
    candidates: candidate.CandidateRepository
    content: content.ContentRepository
    scorer: scorers.Scorer
    summarizer: summarizers.Summarize


def postgres_connection_string():
    username = os.environ["FLARE_POSTGRES_USERNAME"]
    password = os.environ["FLARE_POSTGRES_PASSWORD"]
    host = os.environ["FLARE_POSTGRES_HOST"]
    port = os.environ["FLARE_POSTGRES_PORT"]
    db = os.environ["FLARE_POSTGRES_DB"]
    database = f"postgresql://{username}:{password}@{host}:{port}/{db}"
    return database


def initialize(name: str = "default") -> Backend:
    match name:
        case "default":
            database = postgres_connection_string()
            user_repo = PostgresUserRepository(database)
            content_repo = PostgresContentRepository(database)
            agent_repo = PostgresAgentRepository(database)
            feed_repo = PostgresCandidateRepository(database)
            scorer = OpenAIScorer()
            summarizer = IdentitySummarizer(max_chars=150)
        case _:
            raise ValueError(f"unsupported backend option '{name}'")

    return Backend(
        users=user_repo,
        content=content_repo,
        agents=agent_repo,
        candidates=feed_repo,
        scorer=scorer,
        summarizer=summarizer,
    )
