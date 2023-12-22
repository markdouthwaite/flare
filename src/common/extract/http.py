import requests
from typing import Optional
from .errors import UrlExtractError


def request(
    *,
    url: str,
    method: str,
    user_agent: str,
    accept_language: str,
    custom_headers: Optional[dict],
) -> requests.Response:
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
        return response
    else:
        raise UrlExtractError(f"failed to unfurl target url '{url}'")
