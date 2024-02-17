import math
from typing import List

from flare.common.keywords import count_total_hits
from flare.entities import ExtractedItem


def default_scorer(_: ExtractedItem, value: float = 1.0):
    return value


def total_keyword_hits_scorer(
    item: ExtractedItem,
    keywords: List[str],
    ceiling: float = 25.0,
    steepness: float = 0.2,
):
    hits = count_total_hits(item.content.text, keywords)
    score = ceiling / (1.0 + math.exp(-steepness * hits))
    return score
