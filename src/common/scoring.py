import math
from random import randint, random
from src.entities import ExtractedItem, Post


def decay(s, t, h):
    lmda = math.log2(2) / float(h)
    return s * math.exp(-lmda * t)


def status(post: Post) -> str:
    if post.relevance > 7:
        return "published"
    else:
        return "unpublished"


def featured(post: Post) -> bool:
    if post.relevance > 7 and random() > 0.7 and post.kind != "code":
        return True
    else:
        return False


def relevance(item: IndexedItem) -> int:
    return randint(1, 10)
