from datetime import datetime
from typing import Iterable, Optional, Tuple, Union
from urllib.parse import urlparse

from flare.core import text
from flare.core.errors import LinkValidationError
from flare.core.models.filters import ExtractedLinkFilterSet, LinkFilterSet
from flare.core.models.links import (
    ExtractedLink,
    Link,
    LinkExtractor,
    LinkExtractorConfig,
    RichLink,
    RichLinkConfig,
    RichLinkPostprocessor,
    RichLinkRepository,
    RichLinkSet,
)
from flare.core.models.queries import QueryFilter, QueryFilterSet, QueryOrderBy


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
    attrs = [attribute_scorer(link) for attribute_scorer in config.attribute_scorers]
    rich_link = RichLink(
        id=link.id,
        url=link.url,
        title=link.title,
        description=link.description,
        metadata=link.metadata,
        image=link.image,
        locale=text.locale.detect(link.text.value),
        excerpt=config.summarizer(link.text.value),
        read_time=text.statistics.read_time(link.text.value),
        readability=text.statistics.readability(link.text.value),
        tags=link.tags,
        attributes=dict(attrs),
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
    extracted_link_filter_set: Optional[
        ExtractedLinkFilterSet
    ] = ExtractedLinkFilterSet(),
    rich_link_postprocessors: Optional[Iterable[RichLinkPostprocessor]] = None,
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

        if rich_link_postprocessors is not None:
            for postprocessor in rich_link_postprocessors:
                rich_link = postprocessor(rich_link)

        rich_link_repo.insert(rich_link)
        return rich_link.id

    return _rich_link_extractor


def list_links(payload: dict, repo: RichLinkRepository) -> RichLinkSet:
    if payload.get("filter_set") is not None:
        filters = [QueryFilter(**_) for _ in payload.get("filter_set")]
        filter_set = QueryFilterSet(filters=filters)
    else:
        filter_set = None

    if payload.get("order_by") is not None:
        order_by = QueryOrderBy(**payload.get("order_by"))
    else:
        order_by = None

    limit = payload.get("limit", 10)

    rich_links = repo.list(filter_set=filter_set, order_by=order_by, limit=limit)

    return rich_links


__all__ = [
    "create_rich_link",
    "validate_link",
    "validate_extracted_link",
    "extract_link",
    "domain",
    "init_rich_link_extractor",
    "list_links",
]
