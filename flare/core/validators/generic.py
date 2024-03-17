from typing import List
from flare.core.text import locale as _locale
from flare.core.models.links import ExtractedLink, Link, RichLinkRepository
from flare.core import keywords


def is_allowed(link: Link, block_list: List[str]) -> bool:
    if any(blocked in link.url for blocked in block_list):
        return False
    else:
        return True


def is_english_language(link: ExtractedLink) -> bool:
    locale = _locale.detect(link.text.value)
    if locale in ["en", "en-GB", "en-US"]:
        return True
    else:
        return False


def is_topic(link: ExtractedLink, keyword_list: List[str], min_hits: int = 3) -> bool:
    unique_hits = keywords.count_unique_hits(link.text.value.lower(), keyword_list)

    if unique_hits >= min_hits:
        return True
    else:
        return False


def is_existing(link: Link, repo: RichLinkRepository) -> bool:
    if repo.exists(link.url):
        return False
    else:
        return True
