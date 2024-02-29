from flask import Flask

from flare.common.feeds import load_feed_configs
from flare.common.sources import load_sources
from flare.infrastructure.api.errors import error_handler_blueprint
from flare.infrastructure.api.feeds import feeds_blueprint
from flare.infrastructure.api.posts import posts_blueprint
from flare.infrastructure.api.tasks import tasks_blueprint
from flare.infrastructure.queues import celery


def create_app(settings):
    sources = load_sources(settings)
    feeds = load_feed_configs(settings)

    flask_app = Flask(__name__)
    flask_app.config.from_mapping(
        CELERY={
            "broker_url": settings.BROKER_URL,
            "result_backend": settings.RESULT_BACKEND,
        },
        SOURCES=sources,
        FEEDS=feeds,
        POSTS_REPO=settings.POST_REPOSITORY,
        FEEDS_REPO=settings.FEED_REPOSITORY,
    )

    celery_app = celery.init_app(flask_app)
    celery_app.conf.update(flask_app.config)
    celery_app.conf.update(include=["flare.infrastructure.tasks.posts"])
    flask_app.celery = celery_app

    flask_app.register_blueprint(feeds_blueprint, url_prefix='/api/v1')
    flask_app.register_blueprint(posts_blueprint, url_prefix='/api/v1')
    flask_app.register_blueprint(tasks_blueprint, url_prefix='/api/v1')
    flask_app.register_blueprint(error_handler_blueprint, url_prefix='/api/v1')
    return flask_app, celery_app
