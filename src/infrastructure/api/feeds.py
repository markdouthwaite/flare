import json
from dataclasses import asdict
from flask import Blueprint, current_app, Response

from src.commands.feeds import get_feed

feeds_blueprint = Blueprint("feeds", __name__)


@feeds_blueprint.get("/feeds/<feed_name>")
def get_feed_by_name(feed_name: str):
    feeds_repo = current_app.config["feeds_repo"]
    feed = get_feed(feed_name, feeds_repo)
    return Response(
        json.dumps(asdict(feed), default=lambda _: str(_)),
        content_type="application/json",
    )
