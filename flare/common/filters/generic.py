from flare.common import keywords
from flare.common.extract.metadata import get_locale
from flare.entities import ExtractedItem


def is_english_language(item: ExtractedItem):
    locale = get_locale(item.content.text)
    if locale in ["en", "en-GB", "en-US"]:
        return True
    else:
        return False


def mentions_machine_learning(item: ExtractedItem, min_term_count: int = 2):
    counts = keywords.count_unique_hits(
        item.content.text.lower(), keywords.MACHINE_LEARNING
    )
    if counts >= min_term_count:
        return True
    else:
        return False
