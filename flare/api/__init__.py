from flask import Flask

from flare.api.errors import error_handler_blueprint
from flare.api.links import links_blueprint
from flare.queue.tasks import initialize_celery


def initialize_app(settings):
    flask_app = Flask(__name__)
    flask_app.config.from_mapping(
        RICH_LINKS_REPO=settings.RICH_LINK_REPOSITORY,
        RICH_LINK_EXTRACTORS=settings.RICH_LINK_EXTRACTORS,
        CELERY={
            "broker_url": settings.CELERY_BROKER_URL,
            "result_backend": settings.CELERY_RESULT_BACKEND,
        },
    )
    celery_app = initialize_celery(flask_app)
    celery_app.conf.update(flask_app.config)
    celery_app.conf.update(include=["flare.queue.tasks"])
    flask_app.register_blueprint(links_blueprint, url_prefix="/links")
    flask_app.register_blueprint(error_handler_blueprint)
    flask_app.celery = celery_app
    return flask_app, celery_app
