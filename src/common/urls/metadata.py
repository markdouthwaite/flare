import math
from typing import Optional
from urllib.parse import urlparse
import pycld2 as cld2
from textstat import textstat


def _get_open_graph_property(s, name: str) -> Optional[str]:
    match = s.find("meta", {"property": f"og:{name}"})
    if match is None:
        return match
    else:
        return match["content"]


def _get_twitter_meta(s, name: str) -> Optional[str]:
    match = s.find("meta", {"name": f"twitter:{name}"})
    if match is None:
        match = s.find("meta", {"property": f"twitter:{name}"})

    if match is None:
        return match
    else:
        return match["content"]


def get_open_graph_meta(s):
    return dict(
        title=_get_open_graph_property(s, "title"),
        description=_get_open_graph_property(s, "description"),
        image=_get_open_graph_property(s, "image"),
        type=_get_open_graph_property(s, "type"),
    )


def get_twitter_card_meta(s):
    return dict(
        title=_get_twitter_meta(s, "title"),
        description=_get_twitter_meta(s, "description"),
        image=_get_twitter_meta(s, "image"),
        type=_get_twitter_meta(s, "type"),
    )


def get_meta(soup) -> dict:
    og = get_open_graph_meta(soup)
    tw = get_twitter_card_meta(soup)

    for key, value in tw.items():
        if og[key] is None and value is not None:
            og[key] = value

    return og


def get_read_time(text, wpm: int = 265) -> int:
    return int(math.ceil(len(text.split()) / wpm))


def get_readability(text) -> int:
    return int(math.ceil(textstat.flesch_reading_ease(text)))


def get_locale(text) -> str:
    is_reliable, _, details = cld2.detect(text, isPlainText=True)

    if not is_reliable:
        lang = "unknown"
    elif len(details) > 0 and details[0][1] == "en":
        significant_langs = [_ for _ in details[1:] if _[2] >= 20]
        if len(significant_langs) > 0:
            lang = list(sorted(significant_langs, key=lambda _: -_[2]))[0][1]
        else:
            lang = "en"
    else:
        lang = details[0][1]

    return lang


def postprocess_github_metadata(payload: dict) -> dict:
    """Cleanup GitHub metadata to remove or replace GitHub-specific info."""
    title = payload["url"].replace("https://github.com/", "")
    owner = title.split("/")[0]
    sub_pattern = f"Contribute to {title} development by creating an account on GitHub."
    payload["title"] = title
    payload["description"] = payload["description"].replace(sub_pattern, "").strip()
    payload["description"] = payload["description"].split("- GitHub -")[0].strip()
    payload["image"] = f"https://github.com/{owner}.png"
    return payload


def get_domain(url: str) -> str:
    return urlparse(url).netloc
