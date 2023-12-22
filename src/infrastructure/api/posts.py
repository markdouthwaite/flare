from flask import Blueprint, request, current_app
from src.commands.posts import extract_and_load_post


posts_blueprint = Blueprint("posts", __name__)


@posts_blueprint.post("/posts/extract")
def extract_and_load_posts():
    payload = request.json
    extract_and_load_post(
        payload["url"],
        source=current_app.config["sources"][payload.get("source", "default")],
        repo=current_app.config["posts_repo"],
    )
    return "OK"
