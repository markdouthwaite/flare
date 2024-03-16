from flare.core.models.documents import Document
from flare.core.errors import LinkFetchError
import json
import requests


def default_headers():
    return {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en,en-GB;1=0.5"
    }


def fetch(url: str, headers: dict) -> str:
    headers = default_headers().update(headers)
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.content.decode("utf-8")
    else:
        raise LinkFetchError(f"failed to fetch {url}: {response.status_code}")


def fetch_html(url: str, headers: dict) -> Document:
    data = fetch(url, headers)
    return Document(data, "html.parser")


def fetch_json(url: str, headers: dict) -> dict:
    data = fetch(url, headers)
    return json.loads(data)
