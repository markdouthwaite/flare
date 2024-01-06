from src.entities import Source, Sources
from src.common.extract.metadata import summarize
from src.common.extract import extract
from src.common.scoring import default_scorer
from src.common.plugins import prepare_plugin


def load_sources(s) -> Sources:
    sources = {}
    for key, value in s.SOURCES.items():
        sources[key] = Source(
            name=key,
            kind=value["kind"],
            filters=[prepare_plugin(_) for _ in value.get("filters", [])],
            extractor=prepare_plugin(value.get("extractor", extract)),
            summarizer=prepare_plugin(value.get("summarizer", summarize)),
            scorer=prepare_plugin(value.get("scorer", default_scorer)),
            url_patterns=value.get("url_patterns", {}),
        )

    return sources
