import json
from flask import Blueprint, Response

from flare.core.errors import LinkValidationError

error_handler_blueprint = Blueprint("errors", __name__)


@error_handler_blueprint.app_errorhandler(Exception)
def handle_generic_exception(error: Exception):
    message = {
        "title": "generic-error",
        "message": f"{error}"
    }
    return Response(
        json.dumps(message), status=500, content_type="application/json"
    )


@error_handler_blueprint.app_errorhandler(LinkValidationError)
def handle_link_validation_error(error: LinkValidationError):
    message = {
        "title": "link-validation-error",
        "message": f"{error}"
    }
    return Response(
        json.dumps(message), status=400, content_type="application/json"
    )
