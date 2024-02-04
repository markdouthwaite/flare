from typing import List

from flare.common.extract.metadata import get_locale
from flare.common.keywords import MACHINE_LEARNING as MACHINE_LEARNING_KEYWORDS
from flare.common.keywords import count_unique_hits
from flare.entities import ExtractedItem


def is_english_language(item: ExtractedItem):
    locale = get_locale(item.content.text)
    if locale in ["en", "en-GB", "en-US"]:
        return True
    else:
        return False


def mentions_machine_learning(
    item: ExtractedItem,
    min_term_count: int = 2,
    keywords: List[str] = MACHINE_LEARNING_KEYWORDS,
):
    counts = count_unique_hits(item.content.text.lower(), keywords)
    if counts >= min_term_count:
        return True
    else:
        return False
