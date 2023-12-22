from src.entities import Source, Sources
from src.common.extract.metadata import summarize
from src.common.extract import extract


def load_sources(s) -> Sources:
    sources = {}
    for key, value in s.SOURCES.items():
        sources[key] = Source(
            name=key,
            kind=value["kind"],
            filters=value.get("filters", []),
            extractor=value.get("extractor", extract),
            summarizer=value.get("summarizer", summarize),
            scorer=value.get("scorer", lambda _: 1.0),
            url_patterns=value.get("url_patterns", {}),
        )

    return sources
