import json
from dataclasses import asdict
from flask import Blueprint, request, current_app, Response
from celery import current_app as current_celery_app
from celery.result import AsyncResult
from src.entities.errors import SuccessMessage
from src.common.identifier import generate_id
from src.infrastructure.tasks.posts import extract_and_load_post


posts_blueprint = Blueprint("posts", __name__)


@posts_blueprint.post("/posts/extract")
def extract_and_load_posts():
    payload = request.json
    post_id = generate_id()

    task = extract_and_load_post.delay(
        post_id, payload["url"], source_name=payload.get("source", "default")
    )

    message = SuccessMessage(
        title="extract-submit-success",
        message=f"successfully submitted task '{task.id}' for extraction",
    )

    return Response(
        response=json.dumps(asdict(message)),
        content_type="application/json",
    )


@posts_blueprint.get("/posts/extract/status/<task_id>")
def get_post_extraction_status(task_id: str):
    task = AsyncResult(task_id, app=current_celery_app)
    if task.successful():
        return Response(
            json.dumps(
                {
                    "title": "successful-extraction",
                    "message": "successfully extracted target url",
                }
            )
        )
    elif task.failed():
        return Response(
            json.dumps(
                {
                    "title": "failed-extraction",
                    "message": "failed to extract target url",
                }
            )
        )
    else:
        return Response(
            json.dumps(
                {
                    "title": "pending-extraction",
                    "message": "target url is being extracted, please wait.",
                }
            )
        )


@posts_blueprint.get("/posts/<post_id>")
def get_extracted_post(post_id: str):
    posts_repo = current_app.config["posts_repo"]
    post = posts_repo.get(post_id)
    print(post)
    return Response(
        json.dumps(asdict(post), default=lambda _: str(_)),
        content_type="application/json",
    )


@posts_blueprint.get("/posts")
def get_extracted_posts():
    posts_repo = current_app.config["posts_repo"]
    posts = posts_repo.list()
    return Response(
        json.dumps([asdict(post) for post in posts], default=lambda _: str(_)),
        content_type="application/json",
    )
