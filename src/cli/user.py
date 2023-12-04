import os

import typer
from typing import Optional
import src.commands as cmd
from src.common import backends

EMBED_MODEL = os.environ["FLARE_EMBED_MODEL"]
BACKEND = os.environ.get("FLARE_BACKEND", "default")
backend = backends.initialize(name=BACKEND)

app = typer.Typer()


@app.command()
def create(name: str, slug: str, email: str):
    cmd.user.create_user(backend.users, name, slug, email)


@app.command()
def list():
    users = cmd.user.list_users(backend.users)
    for user in users:
        print(user.dict())


@app.command()
def get(user_id: str):
    user = cmd.user.get_user(backend.users, user_id)
    print(user.dict())


@app.command()
def delete(user_id: str):
    cmd.user.delete_user(backend.users, user_id)
