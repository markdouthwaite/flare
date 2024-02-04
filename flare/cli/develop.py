import importlib.util

import typer

from flare.commands.posts import load_from_disk

app = typer.Typer()


@app.command()
def load_posts_from_disk(path: str, settings_path: str = "settings.py"):
    spec = importlib.util.spec_from_file_location("settings", settings_path)
    settings = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(settings)
    load_from_disk(path, settings.POST_REPOSITORY)
