from typing import Union, Optional, Tuple
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
    RichLinkRepository,
)
from flare.core.errors import LinkValidationError


def domain(url: str) -> str:
    return urlparse(url).netloc


def _validate(
    link: Union[ExtractedLink, Link],
    filter_set: Union[ExtractedLinkFilterSet, LinkFilterSet],
) -> Tuple[bool, Optional[str]]:
    for f in filter_set.filters:
        if not f(link):
            return False, str(f)

    return True, None


def validate_link(link: Link, filter_set: LinkFilterSet) -> Tuple[bool, Optional[str]]:
    return _validate(link, filter_set)


def validate_extracted_link(
    extracted_link: ExtractedLink, filter_set: ExtractedLinkFilterSet
) -> Tuple[bool, Optional[str]]:
    return _validate(extracted_link, filter_set)


def extract_link(
    link: Link, extractor: LinkExtractor, config: LinkExtractorConfig
) -> ExtractedLink:
    return extractor(link, config)


def create_rich_link(link: ExtractedLink, config: RichLinkConfig) -> RichLink:
    rich_link = RichLink(
        id=link.id,
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


def init_rich_link_extractor(
    link_extractor: LinkExtractor,
    link_extractor_config: LinkExtractorConfig,
    rich_link_config: RichLinkConfig,
    rich_link_repo: RichLinkRepository,
    link_filter_set: Optional[LinkFilterSet] = LinkFilterSet(),
    extracted_link_filter_set: Optional[ExtractedLinkFilterSet] = ExtractedLinkFilterSet(),
):
    def _rich_link_extractor(link: Link) -> str:
        valid_link, validation_err = validate_link(link, link_filter_set)

        if not valid_link:
            raise LinkValidationError(f"link validation failed: {validation_err}")

        extracted_link = link_extractor(link, link_extractor_config)

        valid_extracted_link, validation_err = validate_extracted_link(
            extracted_link, extracted_link_filter_set
        )

        if not valid_extracted_link:
            raise LinkValidationError(
                f"extracted link validation failed: {validation_err}"
            )

        rich_link = create_rich_link(extracted_link, rich_link_config)
        rich_link_repo.insert(rich_link)
        return rich_link.id

    return _rich_link_extractor


__all__ = [
    "create_rich_link",
    "validate_link",
    "validate_extracted_link",
    "extract_link",
    "domain",
    "init_rich_link_extractor",
]
