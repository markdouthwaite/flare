from typing import Union
from urllib.parse import urlparse
from datetime import datetime

from flare.core import identifiers, text
from flare.core.models.filters import ExtractedLinkFilterSet, LinkFilterSet
from flare.core.models.links import (
    ExtractedLink,
    Link,
    LinkExtractor,
    LinkExtractorConfig,
    RichLink,
    RichLinkConfig,
)


def domain(url: str) -> str:
    return urlparse(url).netloc


def _validate(
    link: Union[ExtractedLink, Link],
    filter_set: Union[ExtractedLinkFilterSet, LinkFilterSet],
) -> bool:
    for f in filter_set.filters:
        if not f(link):
            return False

    return True


def validate_link(link: Link, filter_set: LinkFilterSet) -> bool:
    return _validate(link, filter_set)


def validate_extracted_link(
    extracted_link: ExtractedLink, filter_set: ExtractedLinkFilterSet
) -> bool:
    return _validate(extracted_link, filter_set)


def extract_link(
    link: Link, extractor: LinkExtractor, config: LinkExtractorConfig
) -> ExtractedLink:
    return extractor(link, config)


def create_rich_link(link: ExtractedLink, config: RichLinkConfig) -> RichLink:
    rich_link = RichLink(
        id=identifiers.generate_id(),
        url=link.url,
        title=link.title,
        description=link.description,
        text=link.text,
        metadata=link.metadata,
        image=link.image,
        locale=text.locale.detect(link.text.value),
        excerpt=config.summarizer(link.text.value),
        read_time=text.statistics.read_time(link.text.value),
        readability=text.statistics.readability(link.text.value),
        tags=link.tags,
        attributes={
            k: v
            for k, v in (
                attribute_scorer(link) for attribute_scorer in config.attribute_scorers
            )
        },
        created_at=datetime.now(),
        updated_at=None,
    )
    return rich_link


__all__ = [
    "create_rich_link",
    "validate_link",
    "validate_extracted_link",
    "extract_link",
    "domain",
]
