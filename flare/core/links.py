from typing import Union
from flare.core.models.links import (Link, ExtractedLink,
                                     RichLink, LinkExtractor, RichLinkConfig)
from flare.core.models.filters import LinkFilterSet, ExtractedLinkFilterSet
from flare.core import text, identifiers


from urllib.parse import urlparse


def domain(url: str) -> str:
    return urlparse(url).netloc


def _validate(link: Union[ExtractedLink, Link], filter_set: Union[ExtractedLinkFilterSet, LinkFilterSet]) -> bool:
    for f in filter_set.filters:
        if f(link):
            return True

    return False


def validate_link(
        link: Link,
        filter_set: LinkFilterSet
) -> bool:
    return _validate(link, filter_set)


def validate_extracted_link(
        extracted_link: ExtractedLink,
        filter_set: ExtractedLinkFilterSet
) -> bool:
    return _validate(extracted_link, filter_set)


def extract_link(link: Link, extractor: LinkExtractor) -> ExtractedLink:
    return extractor(link)


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
            {k: v for k, v in (
                attribute_scorer(link) for attribute_scorer in config.attribute_scorers
            )}
        }
    )
    return rich_link
