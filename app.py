from src.common.sources import load_sources
from src.common.feeds import load_feed_configs
from flask import Flask
from celery import Celery
from src.infrastructure.api.feeds import feeds_blueprint
from src.infrastructure.api.posts import posts_blueprint
from src.infrastructure.api.errors import error_handler_blueprint
import settings

sources = load_sources(settings)
feeds = load_feed_configs(settings)

posts_repo = settings.POST_REPOSITORY
feeds_repo = settings.FEED_REPOSITORY

app = Flask(__name__)
app.config.update(
    {
        "sources": sources,
        "feeds": feeds,
        "posts_repo": posts_repo,
        "feeds_repo": feeds_repo,
    }
)
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"

celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)
app.celery = celery
app.register_blueprint(feeds_blueprint)
app.register_blueprint(posts_blueprint)
app.register_blueprint(error_handler_blueprint)

app.run(port=8080)
