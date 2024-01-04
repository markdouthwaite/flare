from src.common.sources import load_sources
from flask import Flask
from celery import Celery
from src.infrastructure.api.posts import posts_blueprint
from src.infrastructure.api.errors import error_handler_blueprint
import settings

sources = load_sources(settings)
posts_repo = settings.POST_REPOSITORY

app = Flask(__name__)
app.config.update({"sources": sources, "posts_repo": posts_repo})
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"

celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)
app.celery = celery
app.register_blueprint(posts_blueprint)
app.register_blueprint(error_handler_blueprint)

app.run(port=8080)
