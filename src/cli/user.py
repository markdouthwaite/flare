import os

import typer
from typing import Optional
import src.commands as cmd
from src.common import backends

EMBED_MODEL = os.environ["FLARE_EMBED_MODEL"]
BACKEND = os.environ.get("FLARE_BACKEND", "default")
user_repo, _, _ = backends.initialize(name=BACKEND)

app = typer.Typer()


@app.command()
def create(name: str, slug: str, email: str):
    cmd.user.create_user(user_repo, name, slug, email)


@app.command()
def list():
    users = cmd.user.list_users(user_repo)
    for user in users:
        print(user.dict())


@app.command()
def get(user_id: str):
    user = cmd.user.get_user(user_repo, user_id)
    print(user.dict())


@app.command()
def delete(user_id: str):
    cmd.user.delete_user(user_repo, user_id)
