import typer
from . import content, user, agent

app = typer.Typer()
app.add_typer(agent.app, name="agent")
app.add_typer(user.app, name="user")
app.add_typer(content.app, name="content")
