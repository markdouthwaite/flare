import os
import typer
import importlib
from flare.commands.posts import load_from_disk

app = typer.Typer()


@app.command()
def load_posts_from_disk(path: str, settings_module: str = "settings"):
    print(os.listdir("."), os.getcwd())
    settings = importlib.import_module(settings_module)
    load_from_disk(path, settings.POST_REPOSITORY)
