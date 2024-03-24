from trafilatura import extract as extract_html

from flare.core.extractors.common import fetch_html
from flare.core.extractors.metadata import extract as extract_metadata
from flare.core.models.links import (
    ExtractedLink,
    Link,
    LinkExtractorConfig,
    LinkImage,
    LinkText,
)


def extract(link: Link, config: LinkExtractorConfig) -> ExtractedLink:
    doc = fetch_html(link.url, config.get("headers", {}))
    metadata = extract_metadata(doc)
    text = extract_html(str(doc))

    max_chars = config.get("max_chars")

    if max_chars is not None and isinstance(max_chars, int):
        text = text[:max_chars]

    if metadata.get("image") is not None:
        image = LinkImage(url=metadata.get("image"))
    else:
        image = None

    return ExtractedLink(
        id=link.id,
        url=link.url,
        title=metadata.get("title"),
        description=metadata.get("description"),
        text=LinkText(value=text),
        image=image,
        metadata={}
    )
