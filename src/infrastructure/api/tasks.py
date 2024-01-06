import json

from flask import Blueprint, Response
from celery import current_app as current_celery_app
from celery.result import AsyncResult

tasks_blueprint = Blueprint("tasks", __name__)


@tasks_blueprint.get("/tasks/status/<task_id>")
def get_task_status(task_id: str):
    task = AsyncResult(task_id, app=current_celery_app)
    if task.successful():
        return Response(
            json.dumps(
                {
                    "title": "success",
                    "message": "successfully completed task",
                }
            )
        )
    elif task.failed():
        return Response(
            json.dumps(
                {
                    "title": "failure",
                    "message": "failed to complete task",
                }
            )
        )
    else:
        return Response(
            json.dumps(
                {
                    "title": "pending",
                    "message": "task is pending, please wait",
                }
            )
        )
