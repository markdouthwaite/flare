from typing import List, Any, AnyStr
from src.entities.agent import Agent
from src.entities.user import User
from src.interfaces.repositories.agent import AgentRepository
from src.interfaces.repositories.content import ContentRepository

from typing import Protocol
from src.entities.content import Content
from importlib import import_module


class Hook(Protocol):
    def __call__(self, content: Content):
        pass


def load_hook(path: AnyStr) -> Any:
    components = path.split(".")
    module_path = ".".join(components[:-1])
    return getattr(import_module(module_path), components[-1])


def strategy(feed_repo, content_repo, agent, limit=50):
    prompt = "machine learning, generative ai, programming"
    # filter domains domains

    # scan for new content
    # re-rank feed content
    candidates = content_repo.search(prompt, limit=limit)
    for candidate in candidates:
        print(candidate.id, candidate.url, candidate.title)


def create_agent(
    repository: AgentRepository, user: User, name: str, slug: str, hooks: List[str]
):
    agent = Agent(name=name, slug=slug, createdBy=user.slug, hooks=hooks)
    agent_id = agent.id
    repository.create(agent)
    return agent_id


def trigger_agent(
    agent_repo: AgentRepository, content_repo: ContentRepository, agent_id: str
):
    agent = agent_repo.get(agent_id)
    strategy(None, content_repo, agent)
    # print(agent)
    # hooks = [load_hook(hook) for hook in agent.hooks]
    # print(hooks)
