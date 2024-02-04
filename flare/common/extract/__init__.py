from typing import Any, Optional
from urllib.parse import urlparse

import requests

from flare.common.identifier import generate_id
from flare.entities import Content, ExtractedItem

from . import arxiv, github
from .errors import UrlExtractError
from .html import html_parser
from .metadata import get_meta


def _parse_generic(
    url: str,
    res: requests.Response,
    max_chars: int = 3500,
) -> ExtractedItem:
    soup, text, urls = html_parser(res.content, return_urls=True, mask_urls=True)

    meta = get_meta(soup)

    text = text.strip()[:max_chars]

    extracted = ExtractedItem(
        id=generate_id(),
        url=url,
        content=Content(
            title=meta.get("title"), description=meta.get("description"), text=text
        ),
        metadata={},
    )

    return extracted


def default_extract(
    url: str,
    method: str = "GET",
    user_agent: str = "Mozilla/5.0",
    accept_language: str = "en-US,en;q=0.5",
    custom_headers: Optional[dict] = None,
    **kwargs: Any,
):
    custom_headers = custom_headers or {}
    response = requests.request(
        method,
        url,
        headers={
            "User-Agent": user_agent,
            "Accept-Language": accept_language,
            **custom_headers,
        },
    )

    if response.ok:
        return _parse_generic(url, response, **kwargs)
    else:
        raise UrlExtractError(f"failed to unfurl target url '{url}'")


def extract(
    url: str,
    method: str = "GET",
    user_agent: str = "Mozilla/5.0",
    accept_language: str = "en-US,en;q=0.5",
    custom_headers: Optional[dict] = None,
    **kwargs: Any,
) -> ExtractedItem:
    domain = urlparse(url).netloc

    match domain:
        case "arxiv.org":
            adapter = arxiv.extract
        case "github.com":
            adapter = github.extract
        case _:
            adapter = default_extract

    return adapter(
        url,
        method,
        user_agent=user_agent,
        accept_language=accept_language,
        custom_headers=custom_headers,
        **kwargs,
    )
