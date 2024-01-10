from flask import Flask
from src.common.feeds import load_feed_configs
from src.common.sources import load_sources
from src.infrastructure.api.errors import error_handler_blueprint
from src.infrastructure.api.feeds import feeds_blueprint
from src.infrastructure.api.posts import posts_blueprint
from src.infrastructure.api.tasks import tasks_blueprint
from src.infrastructure.queues import celery


def create_app(settings):
    sources = load_sources(settings)
    feeds = load_feed_configs(settings)

    flask_app = Flask(__name__)
    flask_app.config.from_mapping(
        CELERY={
            "broker_url": settings.BROKER_URL,
            "result_backend": settings.RESULT_BACKEND
        },
        SOURCES=sources,
        FEEDS=feeds,
        POSTS_REPO=settings.POST_REPOSITORY,
        FEEDS_REPO=settings.FEED_REPOSITORY,
    )

    celery_app = celery.init_app(flask_app)
    celery_app.conf.update(flask_app.config)

    flask_app.celery = celery_app

    flask_app.register_blueprint(feeds_blueprint)
    flask_app.register_blueprint(posts_blueprint)
    flask_app.register_blueprint(tasks_blueprint)
    flask_app.register_blueprint(error_handler_blueprint)
    return flask_app
