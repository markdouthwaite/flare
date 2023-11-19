import requests
from urllib.parse import urlparse
from typing import Optional, Any
from src.entities.content import RawContent
from src.common.urls.validation import check_url
from src.common.errors.url_unfurl import UrlUnfurlError

from .metadata import get_meta, get_read_time, get_readability, get_locale
from .parser import html_parser


def _parse_generic(
    url: str,
    domain: str,
    res: requests.Response,
    include_body: bool = True,
    max_chars: int = 1500,
) -> RawContent:
    soup, text, urls = html_parser(res.content, return_urls=True, mask_urls=True)

    meta = get_meta(soup)
    read_time = get_read_time(text)
    locale = get_locale(text)
    readability = get_readability(text)

    if not include_body:
        text = None
    else:
        text = text[:max_chars]

    raw_content = RawContent(
        url=url,
        title=meta["title"],
        content={
            "image_url": meta["image"],
            "description": meta["description"],
            "body": text,
        },
        metadata={
            "domain": domain,
            "locale": locale,
            "type": meta.get("type"),
            "readability": readability,
            "read_time": read_time,
            "urls": urls,
        },
    )
    return raw_content


def _parse_response(url: str, res: requests.Response, **kwargs: Any) -> RawContent:
    domain = urlparse(url).netloc

    match domain:
        case _:
            raw_content = _parse_generic(url, domain, res, **kwargs)

    return raw_content


def unfurl(
    url: str,
    method: str = "GET",
    user_agent: str = "Mozilla/5.0",
    accept_language: str = "en-US,en;q=0.5",
    custom_headers: Optional[dict] = None,
    **kwargs: Any,
) -> RawContent:
    check_url(url)
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
        raise UrlUnfurlError(f"failed to unfurl target url '{url}'")
