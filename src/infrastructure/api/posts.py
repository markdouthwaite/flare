import json
from dataclasses import asdict
from flask import Blueprint, request, current_app, Response
from src.entities import SuccessMessage
from src.common.identifier import generate_id


posts_blueprint = Blueprint("posts", __name__)


@posts_blueprint.post("/posts/extract")
def extract_and_load_posts():
    payload = request.json
    post_id = generate_id()

    current_app.celery.send_task(
        "src.infrastructure.tasks.extract_and_load_post",
        args=(post_id, payload["url"]),
        kwargs={
            "source": payload.get("source", "default"),
        },
        task_id=post_id
    )

    message = SuccessMessage(
        title="extract-submit-success",
        message=f"successfully submitted for extraction: {post_id}",
    )

    return Response(
        response=json.dumps(asdict(message)),
        content_type="application/json",
    )


@posts_blueprint.get("/posts/<post_id>")
def get_extracted_post(post_id: str):
    posts_repo = current_app.config["posts_repo"]
    post = posts_repo.get(post_id)
    return Response(
        json.dumps(asdict(post), default=lambda _: str(_)),
        content_type="application/json"
    )


@posts_blueprint.get("/posts")
def get_extracted_posts():
    posts_repo = current_app.config["posts_repo"]
    posts = posts_repo.list()
    return Response(
        json.dumps([asdict(post) for post in posts], default=lambda _: str(_)),
        content_type="application/json"
    )
