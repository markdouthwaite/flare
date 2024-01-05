import math
from random import randint, random
from src.entities import Post, ExtractedItem


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
