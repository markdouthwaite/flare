from flask import Blueprint, current_app, Response, request, jsonify
from flare.core.models.links import Link

links_blueprint = Blueprint("links", __name__)


@links_blueprint.get("/<link_id>")
def get_rich_link(link_id: str):
    rich_links_repo = current_app.config["RICH_LINKS_REPO"]

    rich_link = rich_links_repo.get(link_id)

    return Response(rich_link.json(), content_type="application/json")


@links_blueprint.post("/extract/<extractor>", defaults={"extractor": "html"})
def extract_and_load_link(extractor):
    extractor = current_app.config["RICH_LINK_EXTRACTORS"][extractor]
    payload = request.json
    rich_link_id = extractor(Link(url=payload["url"]))
    return jsonify({"id": f"{rich_link_id}"})
