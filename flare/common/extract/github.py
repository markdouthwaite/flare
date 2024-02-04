import json
from typing import Optional, Tuple

from flare.common.extract import http
from flare.common.identifier import generate_id
from flare.entities import Content, ExtractedItem

from .errors import UrlExtractError

_API_URL = "https://api.github.com/repos/{owner}/{repo_name}"
_RAW_CONTENT_URL = (
    "https://raw.githubusercontent.com/{owner}/{repo_name}/{branch}/{filename}"
)


def get_owner_and_name(url: str) -> Tuple[str, str]:
    return url.split("/")[-2:]


def get_readme(
    owner: str,
    repo_name: str,
    method: str = "GET",
    user_agent: str = "Mozilla/5.0",
    accept_language: str = "en-US,en;q=0.5",
    custom_headers: Optional[dict] = None,
    branches: Tuple[str, ...] = ("master", "main"),
    filenames: Tuple[str, ...] = ("README.md", "readme.md"),
) -> str:
    for branch in branches:
        for filename in filenames:
            url = _RAW_CONTENT_URL.format(
                owner=owner, repo_name=repo_name, branch=branch, filename=filename
            )
            response = http.request(
                url=url,
                method=method,
                user_agent=user_agent,
                accept_language=accept_language,
                custom_headers=custom_headers,
            )
            return response.content.decode("utf-8")

    raise UrlExtractError(
        f"failed to unfurl target github url for '{owner}/{repo_name}'"
    )


def get_details(
    owner: str,
    repo_name: str,
    method: str = "GET",
    user_agent: str = "Mozilla/5.0",
    accept_language: str = "en-US,en;q=0.5",
    custom_headers: Optional[dict] = None,
):
    url = _API_URL.format(owner=owner, repo_name=repo_name)
    response = http.request(
        url=url,
        method=method,
        user_agent=user_agent,
        accept_language=accept_language,
        custom_headers=custom_headers,
    )
    data = json.loads(response.content)

    metadata = {
        "language": data.get("language"),
        "is_fork": data.get("fork", False),
        "is_archived": data.get("archived", False),
        "created_at": data.get("created_at"),
        "updated_at": data.get("updated_at"),
        "topics": data.get("topics", []),
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks", 0),
        "issues": data.get("open_issues_count", 0),
    }

    return {
        "title": data.get("full_name", ""),
        "description": data.get("description", ""),
        "metadata": metadata,
    }


def rewrite_github_url(url: str) -> str:
    return url


def extract(
    url: str,
    method: str = "GET",
    user_agent: str = "Mozilla/5.0",
    accept_language: str = "en-US,en;q=0.5",
    custom_headers: Optional[dict] = None,
    max_chars: int = 3500,
) -> ExtractedItem:
    owner, repo_name = get_owner_and_name(url)
    readme = get_readme(
        owner=owner,
        repo_name=repo_name,
        method=method,
        user_agent=user_agent,
        accept_language=accept_language,
        custom_headers=custom_headers,
    )
    details = get_details(
        owner=owner,
        repo_name=repo_name,
        method=method,
        user_agent=user_agent,
        accept_language=accept_language,
        custom_headers=custom_headers,
    )

    text = readme.strip()[:max_chars]

    extracted = ExtractedItem(
        id=generate_id(),
        url=url,
        content=Content(
            title=details.get("title"),
            description=details.get("description"),
            text=text,
        ),
        metadata=details.get("metadata", {}),
    )

    return extracted
