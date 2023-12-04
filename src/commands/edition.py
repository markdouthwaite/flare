from itertools import islice
from datetime import datetime
from src.entities.agent import Agent
from src.infrastructure.backends import Backend
from src.entities.candidate import Candidate
from src.entities.edition import Edition, Item, Section
from src.commands.candidate import update_candidate


def _is_featured(item):
    if (
        item.attributes.get("completeness", 0.0) >= 4.0
        and item.attributes.get("quality", 0.0) >= 0.4
    ):
        return True
    else:
        return False


def _get_item(backend: Backend, candidate: Candidate) -> Item:
    content = backend.content.get(candidate.content_id)
    return Item(
        id=candidate.content_id,
        url=content.url,
        title=content.title,
        summary=backend.summarizer.summarize(content.content["body"]),
        score=candidate.score,
        featured=candidate.featured,
        published_at=candidate.publishedAt,
        metadata={k: v for k, v in content.metadata_.items() if k not in ["urls"]},
    )


def _get_candidates(backend, k):
    candidates = backend.candidates.list(order_by=Candidate.score.desc())
    top_code = list(islice((_ for _ in candidates if _.type == "code"), k))
    top_research = list(islice((_ for _ in candidates if _.type == "paper"), k))
    top_articles = list(islice((_ for _ in candidates if _.type == "generic"), k))
    selected = [*top_code, *top_research, *top_articles]
    _selected_ids = [_.id for _ in selected]
    unselected = [c for c in candidates if c.id not in _selected_ids]
    return selected, unselected


def _publish(backend, agent, items, allow_featured: bool = False):
    for item in items:
        if item.publishedAt is None:
            item.available = True
            item.publishedAt = datetime.now()

        if allow_featured and _is_featured(item):
            item.featured = True

        update_candidate(backend.candidates, agent, item)


def _unpublish(backend, agent, items):
    for item in items:
        if item.publishedAt is not None:
            item.available = False
            item.featured = False

        update_candidate(backend.candidates, agent, item)


def get_current(backend: Backend) -> Edition:
    items = backend.candidates.list(available=True)

    generic = [_get_item(backend, _) for _ in items if _.type == "generic"]
    code = [_get_item(backend, _) for _ in items if _.type == "code"]
    research = [_get_item(backend, _) for _ in items if _.type == "paper"]

    return Edition(
        sections={
            k: Section(
                featured=[_ for _ in v if _.featured],
                items=[_ for _ in v if not _.featured],
            )
            for k, v in (("generic", generic), ("code", code), ("research", research))
        },
        timestamp=datetime.now().timestamp(),
    )


def update_current(backend: Backend, agent: Agent, k: int = 5):
    publish_list, unpublish_list = _get_candidates(backend, k)
    _publish(backend, agent, publish_list, allow_featured=True)
    _unpublish(backend, agent, unpublish_list)
