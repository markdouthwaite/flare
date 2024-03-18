from datetime import datetime
from typing import Any, Dict, List, Optional

from trafilatura import extract as extract_html

from flare.core.extractors.common import fetch_html
from flare.core.extractors.metadata import extract as extract_metadata
from flare.core.models.documents import Document
from flare.core.models.links import (
    ExtractedLink,
    Link,
    LinkExtractorConfig,
    LinkImage,
    LinkText,
)
from flare.core.models.tags import Tag


def get_citation_date(s: Document) -> str:
    citation_date = s.find("meta", {"name": "citation_date"})["content"]
    date = datetime.strptime(citation_date, "%Y/%m/%d")
    return date.isoformat()


def get_author(s: Document) -> str:
    author = s.find("meta", {"name": "citation_author"})["content"]
    return author


def get_authors(s: Document) -> List[str]:
    authors = s.find_all("meta", {"name": "citation_author"})
    return [_["content"] for _ in authors]


def get_subjects(s: Document) -> List[str]:
    subjects = s.find("td", {"class": "tablecell subjects"})
    return [_.strip() for _ in subjects.text.split(";")]


def get_comments(s: Document) -> Optional[str]:
    comments = s.find("td", {"class": "tablecell comments mathjax"})
    if comments is not None:
        return comments.text.strip()
    else:
        return None


def get_journal_reference(s: Document) -> Optional[str]:
    jref = s.find("td", {"class": "tablecell jref"})
    if jref is not None:
        return jref.text.strip()
    else:
        return None


def get_url(t: Document) -> Optional[str]:
    tag = t.find("p", {"class": "list-title"})
    match = tag.find("a")
    if match is None:
        return None
    else:
        return str(match["href"])


def get_paper_info(doc: Document) -> Dict[str, Any]:
    return {
        "citation_date": get_citation_date(doc),
        "author": get_author(doc),
        "authors": get_authors(doc),
        "subjects": get_subjects(doc),
        "comments": get_comments(doc),
        "journal_ref": get_journal_reference(doc),
    }


def extract(link: Link, config: LinkExtractorConfig) -> ExtractedLink:
    doc = fetch_html(link.url, config.get("headers", {}))
    metadata = extract_metadata(doc)
    text = extract_html(str(doc))
    description = metadata.get("description")
    paper_info = get_paper_info(doc)
    max_chars = config.get("max_chars")

    if max_chars is not None and isinstance(max_chars, int):
        text = text[:max_chars]
        description = description[:max_chars]

    return ExtractedLink(
        id=link.id,
        url=link.url,
        title=metadata.get("title"),
        description=description,
        text=LinkText(value=text),
        image=LinkImage(url=metadata.get("image")),
        metadata=paper_info,
        tags=[Tag(name="arxiv")],
    )
