import json

import requests

from flare.core.errors import LinkFetchError
from flare.core.models.documents import Document


def default_headers():
    return {"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en,en-GB;1=0.5"}


def fetch(url: str, headers: dict) -> str:
    headers = default_headers().update(headers)
    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.content.decode("utf-8")
        else:
            raise LinkFetchError(
                f"failed to fetch {url}: {response.status_code} ({response.content})"
            )
    except ConnectionError as error:
        raise LinkFetchError(f"failed to fetch {url}: connection error") from error


def fetch_html(url: str, headers: dict) -> Document:
    data = fetch(url, headers)
    return Document(data, "html.parser")


def fetch_json(url: str, headers: dict) -> dict:
    data = fetch(url, headers)
    return json.loads(data)
