from flask import Blueprint, Response, current_app, jsonify, request

from flare.core.identifiers import generate_id
from flare.core.links import list_links
from flare.queue.tasks import extract_and_load_link as _extract_and_load_link

links_blueprint = Blueprint("links", __name__)


@links_blueprint.get("/<link_id>")
def get_rich_link(link_id: str):
    rich_links_repo = current_app.config["RICH_LINKS_REPO"]

    rich_link = rich_links_repo.get(link_id)

    return Response(rich_link.json(), content_type="application/json")


@links_blueprint.post("/extract", defaults={"extractor": "html"})
@links_blueprint.post("/extract/<extractor>")
def extract_and_load_link(extractor):
    payload = request.json
    url = payload["url"]

    link_id = generate_id()
    task = _extract_and_load_link.delay(
        link_id=link_id, url=url, extractor_name=extractor
    )
    return jsonify({"id": f"{link_id}", "task": task.id})


@links_blueprint.post("/")
def get_rich_links():
    rich_links_repo = current_app.config["RICH_LINKS_REPO"]
    payload = request.json

    rich_links = list_links(payload, rich_links_repo)

    return Response(rich_links.json(), content_type="application/json")
