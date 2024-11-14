import json

import requests
from requests.exceptions import ConnectionError

from flare.core.errors import LinkFetchError
from flare.core.models.documents import Document


def get_headers(custom_headers: dict) -> dict:
    default_headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en,en-GB;1=0.5",
    }
    if custom_headers:
        default_headers.update(custom_headers)

    return default_headers

def fetch(url: str, custom_headers: dict) -> str:
    """
    Fetches the content from the given URL with optional custom headers.

    Args:
        url (str): The URL to fetch content from.
        custom_headers (dict): A dictionary of custom headers to include in the request.

    Returns:
        str: The content of the response as a decoded string.

    Raises:
        LinkFetchError: If the request fails due to a connection error or a non-OK response status.
    """
    headers = get_headers(custom_headers)

    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.content.decode("utf-8")
        else:
            raise LinkFetchError(
                f"Failed to fetch {url}: {response.status_code} ({response.content})"
            )
    except ConnectionError as error:
        raise LinkFetchError(f"Failed to fetch {url}: Connection error") from error


def fetch_html(url: str, custom_headers: dict) -> Document:
    """
    Fetches the HTML content from the given URL and parses it into a Document object.

    Args:
        url (str): The URL to fetch HTML content from.
        custom_headers (dict): A dictionary of custom headers to include in the request.

    Returns:
        Document: A Document object containing the parsed HTML content.
    """
    data = fetch(url, custom_headers)
    return Document(data, "html.parser")


def fetch_json(url: str, custom_headers: dict) -> dict:
    data = fetch(url, custom_headers)
    return json.loads(data)
