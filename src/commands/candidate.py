from datetime import datetime
from typing import Dict, Optional, List
from src.entities.candidate import Candidate
from src.entities.agent import Agent
from src.infrastructure.backends import Backend
from src.interfaces.repositories.candidate import CandidateRepository

from src.common.metrics import (
    quality_score,
    completeness_score,
    relevance_score,
    aggregate_score,
)


def get_candidate(repository: CandidateRepository, candidate_id: str) -> Candidate:
    return repository.get(candidate_id)


def list_candidate(
    repository: CandidateRepository, limit: Optional[int] = None
) -> List[Candidate]:
    return repository.list(limit=limit)


def list_candidate_ids(
    repository: CandidateRepository, limit: Optional[int] = None
) -> List[str]:
    return repository.list_ids(limit=limit)


def list_candidate_content_ids(
    repository: CandidateRepository, limit: Optional[int] = None
) -> List[str]:
    return repository.list_content_ids(limit=limit)


def insert_candidate(
    repository: CandidateRepository,
    agent: Agent,
    type: str,
    content_id: str,
    attributes: Dict[str, float],
    score: Optional[float] = None,
    available: bool = False,
    featured: bool = False,
):
    item = Candidate(
        content_id=content_id,
        score=score,
        type=type,
        attributes=attributes,
        available=available,
        featured=featured,
        addedBy=agent.slug,
    )
    item_id = item.id

    repository.insert(item)
    return item_id


def update_candidate(repository: CandidateRepository, agent: Agent, item: Candidate):
    item.updatedAt = datetime.now()
    item.updatedBy = agent.slug
    return repository.update(item)


def delete_candidate(repository: CandidateRepository, item: Candidate):
    return repository.delete(item)


def insert_fresh_candidates(
    backend: Backend, agent: Agent, limit: int = 4, max_age: int = 21
):
    existing_feed_items = list_candidate_content_ids(backend.candidates)

    arxiv_items = backend.content.search(
        "generative ai, machine learning engineering, neural networks",
        provider="arxiv",
        exclude_ids=existing_feed_items,
        max_age=max_age,
        limit=limit,
    )

    github_items = backend.content.search(
        "generative ai, machine learning, python programming",
        provider="github",
        exclude_ids=existing_feed_items,
        max_age=max_age,
        limit=limit,
    )

    web_items = backend.content.search(
        "news stories about artificial intelligence,"
        "google, microsoft, amazon, openai, silicon valley, microchips, nvidia",
        provider="hacker_news",
        exclude_ids=existing_feed_items,
        max_age=max_age,
        limit=limit,
    )

    items = [*web_items, *arxiv_items, *github_items]

    # filtered items should be set to unavailable in content records

    # items that can't be inserted should be set to unavailable in content records
    for item in items:
        attribute_scores = {
            "completeness": completeness_score(item),
            "relevance": relevance_score(backend.scorer, item),
            "quality": quality_score(backend.scorer, item),
        }

        match item.provider:
            case "arxiv":
                feed_item_type = "paper"
            case "github":
                feed_item_type = "code"
            case _:
                feed_item_type = "generic"

        insert_candidate(
            backend.candidates,
            agent=agent,
            type=feed_item_type,
            content_id=item.id,
            attributes=attribute_scores,
        )


def update_candidate_scores(backend: Backend, agent: Agent):
    for item in list_candidate(backend.candidates):
        item.score = aggregate_score(item, item.attributes)
        update_candidate(backend.candidates, agent, item)


def reset_candidate_status(backend: Backend, agent: Agent):
    candidates = backend.candidates.list()
    for item in candidates:
        item.available = False
        item.featured = False
        item.publishedAt = None
        update_candidate(backend.candidates, agent, item)
