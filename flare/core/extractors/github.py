from typing import List

from flare.core.errors import LinkExtractError
from flare.core.extractors.common import fetch, fetch_json
from flare.core.models.links import (
    ExtractedLink,
    Link,
    LinkExtractorConfig,
    LinkImage,
    LinkText,
)
from flare.core.models.tags import Tag

_API_URL = "https://api.github.com/repos/{owner}/{repo_name}"
_RAW_CONTENT_URL = (
    "https://raw.githubusercontent.com/{owner}/{repo_name}/{branch}/{filename}"
)
_DEFAULT_BRANCHES = ("master", "main")
_DEFAULT_FILENAMES = ("README.md", "readme.md")


def get_owner_and_name(url: str) -> List[str]:
    return url.split("/")[-2:]


def get_readme(owner: str, repo_name: str, config: LinkExtractorConfig) -> str:
    for branch in config.get("branches", _DEFAULT_BRANCHES):
        for filename in config.get("filenames", _DEFAULT_FILENAMES):
            url = _RAW_CONTENT_URL.format(
                owner=owner, repo_name=repo_name, branch=branch, filename=filename
            )
            return fetch(url, config)

    raise LinkExtractError(
        f"failed to extract readme from target github link for '{owner}/{repo_name}'"
    )


def get_details(
    owner: str, repo_name: str, config: LinkExtractorConfig,
):
    url = _API_URL.format(owner=owner, repo_name=repo_name)
    data = fetch_json(url, config)

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
        "image": f"https://github.com/{owner}.png",
        "metadata": metadata,
    }


def extract(link: Link, config: LinkExtractorConfig) -> ExtractedLink:
    owner, repo_name = get_owner_and_name(link.url)
    max_chars = config.get("max_chars")

    readme = get_readme(owner=owner, repo_name=repo_name, config=config,)

    if max_chars is not None and isinstance(max_chars, int):
        readme = readme[:max_chars]

    details = get_details(owner=owner, repo_name=repo_name, config=config,)

    return ExtractedLink(
        url=link.url,
        title=details.get("title"),
        description=details.get("description"),
        text=LinkText(value=readme),
        image=LinkImage(url=details.get("image")),
        metadata=details.get("metadata"),
        tags=[Tag(name="arxiv")],
    )
