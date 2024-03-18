from flask import Flask

from flare.api.links import links_blueprint
from flare.api.errors import error_handler_blueprint
from flare.core.models.links import RichLinkRepository


def initialize_app(rich_link_extractors: dict, rich_link_repo: RichLinkRepository):
    flask_app = Flask(__name__)
    flask_app.config.from_mapping(
        RICH_LINKS_REPO=rich_link_repo, RICH_LINK_EXTRACTORS=rich_link_extractors
    )

    flask_app.register_blueprint(links_blueprint, url_prefix="/links")
    flask_app.register_blueprint(error_handler_blueprint)
    return flask_app
