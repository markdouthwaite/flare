import uuid
import json
import pandas as pd
from datetime import datetime
from typing import Iterable, Dict, Any
from src.entities import IndexedItem, Content
from src.common import locale
from urllib.parse import urljoin, urlparse
from src.common.identifier import generate_id


def rewrite_github_api_url(url: str) -> str:
    owner, repo = url.split("/")[-2:]
    return f"https://github.com/{owner}/{repo}"


def rewrite_url(url: str) -> str:
    return urljoin(url, urlparse(url).path)


def _github_to_indexed_item(s: Dict[str, Any]) -> IndexedItem:
    content = json.loads(s["content"])
    metadata = json.loads(s["metadata"])
    statistics = json.loads(s["statistics"])
    url = rewrite_github_api_url(s["url"])
    owner = url.split("/")[-2]
    image_url = f"https://github.com/{owner}.png"
    text = content.get("readme", "")
    return IndexedItem(
        id=generate_id(),
        url=url,
        source="github",
        locale=locale.detect(text),
        content=Content(title=content.get("title"), text=text, image_url=image_url),
        metadata=dict(
            created_at=metadata["created_at"],
            updated_at=metadata["updated_at"],
            language=metadata["language"],
            topics=metadata["topics"],
            is_fork=metadata["is_fork"],
            is_archived=metadata["is_archived"],
            forks=statistics["forks"],
            stars=statistics["stars"],
            issues=statistics["issues"],
        ),
        indexed_at=datetime.now(),
        indexed_by="default",
    )


def _hacker_news_to_indexed_item(s: Dict[str, Any]) -> IndexedItem:
    content = json.loads(s["content"])
    metadata = json.loads(s["metadata"])
    text = content["text"]
    return IndexedItem(
        id=generate_id(),
        url=rewrite_url(s["url"]),
        source="hacker_news",
        locale=locale.detect(text),
        content=Content(
            text=text, title=metadata.get("title"), image_url=metadata.get("image")
        ),
        metadata=dict(),
        indexed_at=datetime.now(),
        indexed_by="default",
    )


def _arxiv_to_indexed_item(s: Dict[str, Any]) -> IndexedItem:
    content = json.loads(s["content"])
    metadata = json.loads(s["metadata"])
    text = content["text"]
    return IndexedItem(
        id=generate_id(),
        url=rewrite_url(s["url"]),
        source="arxiv",
        locale=locale.detect(text),
        content=Content(text=text, image_url=metadata.get("image")),
        metadata=dict(
            lead_author=metadata.get("lead_author"),
            authors=metadata.get("authors", []),
            journal_reference=metadata.get("journal_reference"),
            published_at=metadata.get("published_at"),
            subjects=metadata.get("subjects", []),
        ),
        indexed_at=datetime.now(),
        indexed_by="default",
    )


def to_indexed_item(s: Dict[str, Any]) -> IndexedItem:
    match s["provider"]:
        case "github":
            return _github_to_indexed_item(s)
        case "hacker_news":
            return _hacker_news_to_indexed_item(s)
        case "arxiv":
            return _arxiv_to_indexed_item(s)
        case _:
            raise ValueError(f"unknown provider '{s['provider']}'")
