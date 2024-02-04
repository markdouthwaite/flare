import typer
from flare.cli import develop

app = typer.Typer()
app.add_typer(develop.app, name="develop")

__all__ = ["app"]
