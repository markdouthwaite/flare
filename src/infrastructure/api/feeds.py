import json
from dataclasses import asdict
from flask import Blueprint, current_app, Response, request
from src.entities.errors import SuccessMessage
from src.commands.feeds import get_feed
from src.infrastructure.tasks.feeds import create_or_update_feed

feeds_blueprint = Blueprint("feeds", __name__)


@feeds_blueprint.get("/feeds/<feed_name>")
def get_feed_by_name(feed_name: str):
    feeds_repo = current_app.config["FEEDS_REPO"]
    feed = get_feed(feed_name, feeds_repo)
    return Response(
        json.dumps(asdict(feed), default=lambda _: str(_)),
        content_type="application/json",
    )


@feeds_blueprint.post("/feeds/update")
def update_feed():
    name = request.json["name"]

    task = create_or_update_feed.delay(
        name,
    )

    message = SuccessMessage(
        title="extract-submit-success",
        message=f"successfully submitted task '{task.id}' to update feed '{name}'",
    )

    return Response(json.dumps(asdict(message)), content_type="application/json")
