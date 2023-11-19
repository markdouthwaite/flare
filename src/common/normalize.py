import json
import pycld2
from src.common.urls.metadata import get_locale, get_domain
from src.entities.content import RawContent


def normalize_github_record(record):
    content = record["content"]
    metadata = record["metadata"]
    statistics = record["statistics"]
    path = "/".join(record["url"].split("/")[-2:])
    url = f"https://github.com/{path}"

    if content["readme"] is None:
        return None
    if len(content["readme"]) < 1500:
        return None

    try:
        locale = get_locale(content["readme"])
    except pycld2.error:
        locale = None

    raw_content = RawContent(
        url=url,
        title=metadata["full_name"],
        provider="github",
        content={"body": content["readme"], "description": metadata["description"]},
        metadata={
            "domain": get_domain(record["url"]),
            "stars": statistics["stars"],
            "forks": statistics["forks"],
            "issues": statistics["issues"],
            "language": metadata["language"],
            "locale": locale,
            "is_fork": metadata["is_fork"],
            "is_archived": metadata["is_archived"],
        },
        tags=metadata["topics"],
    )
    return raw_content


def normalize_hacker_news_record(record):
    content = record["content"]
    metadata = record["metadata"]
    statistics = record["statistics"]

    if metadata["title"] is None:
        return None

    try:
        locale = get_locale(content["text"])
    except pycld2.error:
        locale = None

    raw_content = RawContent(
        url=record["url"],
        title=metadata["title"],
        provider="hacker_news",
        content={
            "image_url": metadata["image"],
            "body": content["text"],
            "description": metadata["description"],
        },
        metadata={
            "domain": get_domain(record["url"]),
            "locale": locale,
            "read_time": statistics["read_time"],
            "readability": statistics["readability"],
            "urls": content["urls"],
        },
        tags=[],
    )
    return raw_content


def normalize_arxiv_record(record):
    content = record["content"]
    metadata = record["metadata"]
    statistics = record["statistics"]
    raw_content = RawContent(
        url=record["url"],
        title=metadata["title"],
        provider="arxiv",
        content={
            "image_url": metadata["image"],
            "body": content["text"],
            "description": metadata["description"],
        },
        metadata={
            "domain": get_domain(record["url"]),
            "journal_reference": metadata["journal_reference"],
            "authors": metadata["authors"],
            "locale": metadata["language"],
            "read_time": statistics["read_time"],
            "readability": statistics["readability"],
            "published_at": metadata["published_at"],
            "subjects": metadata["subjects"],
            "urls": content["urls"],
        },
        tags=[],
    )
    return raw_content


def normalize_legacy_record(record):
    match record["provider"]:
        case "github":
            return normalize_github_record(record)
        case "arxiv":
            return normalize_arxiv_record(record)
        case "hacker_news":
            return normalize_hacker_news_record(record)
