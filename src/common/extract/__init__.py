import requests
from urllib.parse import urlparse
from typing import Optional, Any
from src.entities import ExtractedItem, Content
from src.common.identifier import generate_id
from .metadata import get_meta
from .html import html_parser
from .errors import UrlExtractError


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


def _parse_response(url: str, res: requests.Response, **kwargs: Any) -> ExtractedItem:
    domain = urlparse(url).netloc

    match domain:
        case _:
            raw_content = _parse_generic(url, res, **kwargs)

    return raw_content


def extract(
    url: str,
    method: str = "GET",
    user_agent: str = "Mozilla/5.0",
    accept_language: str = "en-US,en;q=0.5",
    custom_headers: Optional[dict] = None,
    **kwargs: Any,
) -> ExtractedItem:
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
        return _parse_response(url, response, **kwargs)
    else:
        raise UrlExtractError(f"failed to unfurl target url '{url}'")
