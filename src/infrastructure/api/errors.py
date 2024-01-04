import json
from dataclasses import asdict
from flask import Blueprint, Response
from src.common.errors import PostReposistoryReadError
from src.common.extract.errors import UrlExtractError
from src.entities import ErrorMessage


error_handler_blueprint = Blueprint("errors", __name__)


@error_handler_blueprint.app_errorhandler(UrlExtractError)
def handle_url_extraction_error(error: UrlExtractError):
    message = ErrorMessage(title="url-extract-error", message=error.args[0])

    return Response(
        json.dumps(asdict(message)), status=400, content_type="application/json"
    )


@error_handler_blueprint.app_errorhandler(PostReposistoryReadError)
def handle_post_repository_read_error(error: PostReposistoryReadError):
    message = ErrorMessage(title="repository-read-error", message=error.args[0])

    return Response(
        json.dumps(asdict(message)), status=400, content_type="application/json"
    )
