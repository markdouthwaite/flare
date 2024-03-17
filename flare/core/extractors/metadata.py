from typing import Dict, Optional

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


def head_metadata(doc: Document):
    title = doc.title.text
    if title is None:
        title = doc.h1.text

    if title is None:
        metadata = {}
    else:
        metadata = dict(title=title)
    return metadata


def extract(doc: Document) -> Dict[str, Optional[str]]:
    head = head_metadata(doc)
    og = open_graph_metadata(doc)
    tw = twitter_metadata(doc)

    metadata = dict()

    # the priority of metadata fields is captured in the order of the meta fields
    # we prefer open graph, then twitter, then info in the head tag
    for meta in (og, tw, head):
        for k, v in meta.items():
            if metadata.get(k) is None:
                metadata[k] = v

    return metadata
