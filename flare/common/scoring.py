import math
from random import randint, random
from typing import List

from flare.common.keywords import count_total_hits
from flare.entities import ExtractedItem, Post


def decay(s, t, h):
    _lambda = math.log2(2) / float(h)
    return s * math.exp(-_lambda * t)


def status(post: Post) -> str:
    if post.rating > 7:
        return "published"
    else:
        return "unpublished"


def featured(post: Post) -> bool:
    if post.rating > 7 and random() > 0.7 and post.kind != "code":
        return True
    else:
        return False


def relevance(_: ExtractedItem) -> int:
    return randint(1, 10)


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
