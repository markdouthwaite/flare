from flask import Flask
from celery import current_app, shared_task, Celery, Task
from flare.core.models.links import Link


@shared_task(ignore_result=False)
def extract_and_load_link(link_id: str, url: str, extractor_name: str):
    extractor = current_app.conf["RICH_LINK_EXTRACTORS"][extractor_name]
    extractor(Link(url=url, id=link_id))


def initialize_celery(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
