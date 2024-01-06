from src.common.sources import load_sources
from src.common.feeds import load_feed_configs
from flask import Flask
from src.infrastructure.queues import celery
from src.infrastructure.api.feeds import feeds_blueprint
from src.infrastructure.api.posts import posts_blueprint
from src.infrastructure.api.errors import error_handler_blueprint
import settings


sources = load_sources(settings)
feeds = load_feed_configs(settings)

posts_repo = settings.POST_REPOSITORY
feeds_repo = settings.FEED_REPOSITORY

flask_app = Flask(__name__)
flask_app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://0.0.0.0:6379/0",
        result_backend="redis://0.0.0.0:6379/0",
        task_ignore_result=True,
        imports=("src.infrastructure.tasks", )
    ),
    SOURCES=sources,
    FEEDS=feeds,
    POSTS_REPO=posts_repo,
    FEEDS_REPO=feeds_repo
)

celery_app = celery.init_app(flask_app)
celery_app.conf.update(
    flask_app.config
)

flask_app.celery = celery_app

flask_app.register_blueprint(feeds_blueprint)
flask_app.register_blueprint(posts_blueprint)
flask_app.register_blueprint(error_handler_blueprint)
