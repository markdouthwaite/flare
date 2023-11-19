import os

import typer
from typing import List
import src.commands as cmd
from src.common import backends


BACKEND = os.environ.get("FLARE_BACKEND", "default")
user_repo, content_repo, agent_repo = backends.initialize(name=BACKEND)

app = typer.Typer()


@app.command()
def create(user_id: str, name: str, slug: str, hooks: List[str]):
    user = user_repo.get(user_id)
    agent_id = cmd.agent.create_agent(agent_repo, user, name, slug, hooks)
    print(agent_id)


@app.command()
def trigger(agent_id: str):
    cmd.agent.trigger_agent(agent_repo, content_repo, agent_id)
