from src.common.sources import load_sources
from flask import Flask
from src.infrastructure.api.posts import posts_blueprint
import settings

sources = load_sources(settings)
posts_repo = settings.POST_REPOSITORY

app = Flask(__name__)
app.config.update({"sources": sources, "posts_repo": posts_repo})
app.register_blueprint(posts_blueprint)
# extract_and_load_post("https://github.com/markdouthwaite/xanthus", sources["github"], repo)
# print(repo.list())

app.run(port=8080)
