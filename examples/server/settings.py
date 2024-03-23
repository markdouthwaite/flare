from flare.core.models.links import RichLinkConfig
from flare.core.models.filters import LinkFilterSet, ExtractedLinkFilterSet
from flare.core.links import init_rich_link_extractor
from flare.core.validators.generic import (
    is_topic,
    is_allowed,
    is_english_language,
    is_existing,
)
from flare.core.validators.github import (
    is_active_repo,
    is_popular_repo,
    is_not_malware_repo,
)
from flare.core.extractors import github, arxiv, html
from firebase_admin import initialize_app as initialize_firebase_app
from flare.db.links.firestore import FirestoreRichLinkRepository
from flare.core.keywords import machine_learning
from functools import partial

from utils import machine_learning_relevance, summarize as openai_summarizer


firebase_app = initialize_firebase_app()

CELERY_BROKER_URL = "redis://0.0.0.0:6379/0"
CELERY_RESULT_BACKEND = "redis://0.0.0.0:6379/0"

RICH_LINK_REPOSITORY = FirestoreRichLinkRepository(firebase_app, "links")
RICH_LINK_EXTRACTORS = {
    "html": init_rich_link_extractor(
        link_extractor=html.extract,
        link_extractor_config={},
        rich_link_config=RichLinkConfig(
            summarizer=openai_summarizer,
            attribute_scorers=[machine_learning_relevance],
        ),
        rich_link_repo=RICH_LINK_REPOSITORY,
        link_filter_set=LinkFilterSet(
            filters=[
                partial(is_allowed, block_list=["youtube.com"]),
                partial(is_existing, repo=RICH_LINK_REPOSITORY),
            ]
        ),
        extracted_link_filter_set=ExtractedLinkFilterSet(
            filters=[
                is_english_language,
                partial(is_topic, keyword_list=machine_learning.KEYWORDS),
            ]
        ),
    ),
    "github": init_rich_link_extractor(
        link_extractor=github.extract,
        link_extractor_config={},
        rich_link_config=RichLinkConfig(
            summarizer=openai_summarizer,
            attribute_scorers=[machine_learning_relevance],
        ),
        rich_link_repo=RICH_LINK_REPOSITORY,
        link_filter_set=LinkFilterSet(
            filters=[partial(is_existing, repo=RICH_LINK_REPOSITORY)]
        ),
        extracted_link_filter_set=ExtractedLinkFilterSet(
            filters=[
                is_not_malware_repo,
                is_active_repo,
                is_popular_repo,
                is_english_language,
                partial(is_topic, keyword_list=machine_learning.KEYWORDS),
            ]
        ),
    ),
    "arxiv": init_rich_link_extractor(
        link_extractor=arxiv.extract,
        link_extractor_config={},
        rich_link_config=RichLinkConfig(
            summarizer=openai_summarizer,
            attribute_scorers=[machine_learning_relevance],
        ),
        rich_link_repo=RICH_LINK_REPOSITORY,
        link_filter_set=LinkFilterSet(
            filters=[partial(is_existing, repo=RICH_LINK_REPOSITORY)]
        ),
        extracted_link_filter_set=ExtractedLinkFilterSet(
            filters=[
                is_english_language,
                partial(is_topic, keyword_list=machine_learning.KEYWORDS),
            ]
        ),
    ),
}
