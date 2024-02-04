from datetime import datetime
from typing import Any, Dict, List, Optional

import requests

from flare.common.identifier import generate_id
from flare.entities import Content, ExtractedItem, HtmlDocument

from .errors import UrlExtractError
from .html import html_parser
from .metadata import get_meta as get_generic_metadata


def get_citation_date(s: HtmlDocument) -> str:
    citation_date = s.find("meta", {"name": "citation_date"})["content"]
    date = datetime.strptime(citation_date, "%Y/%m/%d")
    return date.isoformat()


def get_author(s: HtmlDocument) -> str:
    author = s.find("meta", {"name": "citation_author"})["content"]
    return author


def get_authors(s: HtmlDocument) -> List[str]:
    authors = s.find_all("meta", {"name": "citation_author"})
    return [_["content"] for _ in authors]


def get_subjects(s: HtmlDocument) -> List[str]:
    subjects = s.find("td", {"class": "tablecell subjects"})
    return [_.strip() for _ in subjects.text.split(";")]


def get_comments(s: HtmlDocument) -> Optional[str]:
    comments = s.find("td", {"class": "tablecell comments mathjax"})
    if comments is not None:
        return comments.text.strip()
    else:
        return None


def get_journal_reference(s: HtmlDocument) -> Optional[str]:
    jref = s.find("td", {"class": "tablecell jref"})
    if jref is not None:
        return jref.text.strip()
    else:
        return None


def get_url(t: HtmlDocument) -> Optional[str]:
    tag = t.find("p", {"class": "list-title"})
    match = tag.find("a")
    if match is None:
        return None
    else:
        return str(match["href"])


def get_paper_info(doc: HtmlDocument) -> Dict[str, Any]:
    return {
        "citation_date": get_citation_date(doc),
        "author": get_author(doc),
        "authors": get_authors(doc),
        "subjects": get_subjects(doc),
        "comments": get_comments(doc),
        "journal_ref": get_journal_reference(doc),
    }


def _parse_response(
    url: str,
    res: requests.Response,
    max_chars: int = 3500,
) -> ExtractedItem:
    soup, text, urls = html_parser(res.content, return_urls=True, mask_urls=True)
    meta = get_generic_metadata(soup)
    info = get_paper_info(soup)
    text = text.strip()[:max_chars]

    extracted = ExtractedItem(
        id=generate_id(),
        url=url,
        content=Content(
            title=meta.get("title"), description=meta.get("description"), text=text
        ),
        metadata=info,
    )

    return extracted


def extract(
    url: str,
    method: str = "GET",
    user_agent: str = "Mozilla/5.0",
    accept_language: str = "en-US,en;q=0.5",
    custom_headers: Optional[dict] = None,
    **kwargs: Any,
) -> ExtractedItem:
    custom_headers = custom_headers or {}
    response = requests.request(
        method,
        url,
        headers={
            "User-Agent": user_agent,
            "Accept-Language": accept_language,
            **custom_headers,
        },
    )

    if response.ok:
        return _parse_response(url, response, **kwargs)
    else:
        raise UrlExtractError(f"failed to unfurl target url '{url}'")
