import json
from dataclasses import asdict
from flask import Blueprint, request, current_app, Response
from src.commands.posts import extract_and_load_post
from src.common.extract.errors import UrlExtractError
from src.entities import ErrorMessage, SuccessMessage


posts_blueprint = Blueprint("posts", __name__)


@posts_blueprint.post("/posts/extract")
def extract_and_load_posts():
    payload = request.json
    try:
        extract_and_load_post(
            payload["url"],
            source=current_app.config["sources"][payload.get("source", "default")],
            repo=current_app.config["posts_repo"],
        )
        message = SuccessMessage(
            title="success", message="successfully extracted target url"
        )
        status = 200

    except UrlExtractError as e:
        message = ErrorMessage(
            title="error", message=f"failed to extract target url: {e}"
        )
        status = 400

    return Response(
        status=status,
        response=json.dumps(asdict(message)),
        content_type="application/json",
    )
