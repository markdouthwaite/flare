from src.entities import ExtractedItem
from datetime import datetime
from src.common.keywords import count_unique_hits


def validate_github_repo_language(item: ExtractedItem, languages: set) -> bool:
    match item.source:
        case "github":
            language = item.metadata.get("language")
            if language in languages:
                return True
            else:
                return False
        case _:
            return True


def validate_is_active_github_repo(
    item: ExtractedItem, last_active_in_days: int
) -> bool:
    match item.source:
        case "github":
            updated_at = item.metadata.get("updated_at")
            timestamp = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ")
            if (datetime.now() - timestamp).days <= last_active_in_days:
                return True
            else:
                return False
        case _:
            return True


def validate_locale(item: ExtractedItem, locales: set) -> bool:
    if item.locale in locales:
        return True
    else:
        return False


def validate_domain(item: ExtractedItem, excluded_domains: set) -> bool:
    if any(domain in item.url for domain in excluded_domains):
        return False
    else:
        return True


def validate_content_text_length(item: IndexedItem, min_length: int) -> bool:
    if len(item.content.text) < min_length:
        return False
    else:
        return True


def validate_keywords(item: IndexedItem, keywords: list, min_hits: int) -> bool:
    if count_unique_hits(item.content.text.lower(), keywords) >= min_hits:
        return True
    else:
        return False


def validate_unique_url(item: IndexedItem, urls: set) -> bool:
    if item.url in urls:
        return False
    else:
        return True


def validate_title(item: ExtractedItem) -> bool:
    if item.content.title is not None and len(item.content.title) > 0:
        return True
    else:
        return False


def validate_github_origin(item: IndexedItem) -> bool:
    # check that a repo is sourced from the GitHub crawler, not via alternative source
    if item.source == "hacker_news" and "github.com" in item.url:
        return False
    return True


def validate_awesome_lists(item: ExtractedItem) -> bool:
    if item.source == "github" and "awesome-" in item.content.title:
        return False
    else:
        return True


def validate_restricted_terms(item: ExtractedItem) -> bool:
    terms = ["porn"]
    if any(term in item.content.text.lower() for term in terms):
        return False
    else:
        return True


def validate_arxiv_origin(item: ExtractedItem) -> bool:
    if item.source == "hacker_news" and "arxiv.org" in item.url:
        return False
    else:
        return True


def validate_github_repo_popularity(item: ExtractedItem, min_stars: int) -> bool:
    if item.source == "github" and item.metadata.get("stars", 0) < min_stars:
        return False
    else:
        return True
