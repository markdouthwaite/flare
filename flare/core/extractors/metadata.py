from typing import Optional, Dict

from flare.core.models.documents import Document


def open_graph_property(doc: Document, name: str) -> Optional[str]:
    match = doc.find("meta", {"property": f"og:{name}"})
    if match is None:
        return match
    else:
        return match["content"]


def twitter_property(doc: Document, name: str) -> Optional[str]:
    match = doc.find("meta", {"name": f"twitter:{name}"})
    if match is None:
        match = doc.find("meta", {"property": f"twitter:{name}"})

    if match is None:
        return match
    else:
        return match["content"]


def open_graph_metadata(doc: Document) -> Dict[str, Optional[str]]:
    return {
        "title": open_graph_property(doc, "title"),
        "description": open_graph_property(doc, "description"),
        "image": open_graph_property(doc, "image"),
        "type": open_graph_property(doc, "type"),
    }


def twitter_metadata(doc: Document):
    return {
        "title": twitter_property(doc, "title"),
        "description": twitter_property(doc, "description"),
        "image": twitter_property(doc, "image"),
        "type": twitter_property(doc, "type"),
    }


def extract(doc: Document) -> Dict[str, Optional[str]]:
    og = open_graph_metadata(doc)
    tw = twitter_metadata(doc)

    for key, value in tw.items():
        if og[key] is None and value is not None:
            og[key] = value

    return og
