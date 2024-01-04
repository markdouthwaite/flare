from src.entities import Post
from src.common import keywords


def is_english_language(post: Post):
    if post.locale in ["en", "en-GB", "en-US"]:
        return True
    else:
        return False


def mentions_machine_learning(post: Post, min_term_count: int = 2):
    counts = keywords.count_unique_hits(post.text.lower(), keywords.MACHINE_LEARNING)
    if counts >= min_term_count:
        return True
    else:
        return False
