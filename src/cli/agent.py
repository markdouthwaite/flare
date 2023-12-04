import os

import typer
from typing import List
import src.commands as cmd
from src.common import backends


BACKEND = os.environ.get("FLARE_BACKEND", "default")
backend = backends.initialize(name=BACKEND)

app = typer.Typer()


@app.command()
def create(user_id: str, name: str, slug: str, hooks: List[str] = None):
    user = backend.users.get(user_id)
    agent_id = cmd.agent.create_agent(backend.agents, user, name, slug, hooks)
    print(agent_id)


@app.command()
def trigger(agent_id: str):
    cmd.agent.trigger_agent(backend.agents, backend.content, agent_id)
