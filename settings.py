from src.infrastructure.repositories.posts import ParquetPostRepository
from src.infrastructure.repositories.feeds import LocalFeedRepository
from src.common.extract import arxiv, github
from src.common import filters, feeds

POST_REPOSITORY = ParquetPostRepository(
    "data/development/posts.parquet", primary_key="url"
)

FEED_REPOSITORY = LocalFeedRepository("data/development/feeds")


SOURCES = {
    "default": {
        "kind": "article",
        "filters": [
            filters.generic.is_english_language,
            filters.generic.mentions_machine_learning,
        ],
        "url_patterns": {
            "restrict": [r"https?://(?:\w+\.)?youtube\.com(?:/[\w/#!.-]*)?"],
            "allow": [
                # r"https?://(?:\w+\.)?douthwaite\.io(?:/[\w/#!.-]*)?"
            ],
        },
    },
    "github": {
        "kind": "code",
        "extractor": github.extract,
        "filters": [
            filters.github.is_popular_repo,
            filters.github.is_not_malware_repo,
            filters.github.is_active_repo,
            # filters.github.is_python_repo,
            filters.generic.is_english_language,
            filters.generic.mentions_machine_learning,
        ],
    },
    "arxiv": {
        "kind": "paper",
        "extractor": arxiv.extract,
        "filters": [
            filters.generic.is_english_language,
            filters.generic.mentions_machine_learning,
        ],
    },
}

FEEDS = {"firehose": {"builder": feeds.firehose, "kwargs": {}}}
