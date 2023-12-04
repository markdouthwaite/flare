from datetime import datetime
from math import exp, log2


def _score(scorer, content, prompt: str) -> float:
    if content.content.get("body") is None:
        return 1
    if len(content.content.get("body")) < 250:
        return 1
    score = scorer.score(prompt, content.content.get("body"))
    print(content.url, score)
    return score / 10.0


def relevance_score(scorer, content) -> float:
    prompt = (
        "You are a machine learning engineer. Score responses as integer values "
        "out of 10 based on how interesting you think provided text is. Provide "
        "no other output."
    )
    return _score(scorer, content, prompt)


def quality_score(scorer, content) -> float:
    prompt = """
    You are an expert editor. Score responses as out of 10 based on how 
    well-written you think provided text is. Provide the answer as a single digit 
    integer. Provide no other output.
    """
    return _score(scorer, content, prompt)


def completeness_score(content) -> int:
    match content.provider:
        case "hacker_news":
            score = 0
            down_weighted_domains = ["www.nytimes.com", "www.wsj.com", "old.reddit.com"]
            if content.content.get("image_url") is not None:
                score += 1
            if content.metadata_.get("read_time", 0) > 4:
                score += 1
            if content.metadata_.get("locale", None) in ("en", "en-US", "en-GB"):
                score += 1
            if content.metadata_.get("readability", 100) < 40:
                score += 1
            if content.metadata_.get("domain") not in down_weighted_domains:
                score += 1
        case _:
            score = 0
    return score


def aggregate_score(item, attributes, half_life=21, featured_multiplier=2) -> float:
    if item.featured:
        half_life *= featured_multiplier

    if item.publishedAt is not None:
        td = (datetime.now() - item.publishedAt).days
        lmda = log2(2) / float(half_life)
        decay = exp(-lmda * td)
    else:
        decay = 1.0
    agg_score = attributes["quality"] * attributes["relevance"]
    return agg_score * decay
