from functools import partial

from firebase_admin import initialize_app

from flare.core.embeddings import embed_text
from flare.core.extractors import html
from flare.core.links import init_rich_link_extractor
from flare.core.models.filters import ExtractedLinkFilterSet
from flare.core.models.links import Link, RichLinkConfig
from flare.db.links.firestore import FirestoreRichLinkRepository

firebase_app = initialize_app()

rich_link_repo = FirestoreRichLinkRepository(firebase_app, "rich_links")

rich_link_config = RichLinkConfig(
    summarizer=lambda _: _, attribute_scorers=[lambda _: ("sample", 1)],
    embedding_model=partial(embed_text, path="data/models/all-MiniLM-L6-v2"),
)

link_extractor_config = {}

rich_link_extractor = init_rich_link_extractor(
    html.extract,
    link_extractor_config,
    rich_link_config,
    rich_link_repo,
    extracted_link_filter_set=ExtractedLinkFilterSet(
        filters=[lambda _: _.url != "https://mark.douthwaite.io"]
    ),
)

rich_link_extractor(Link(url="https://mark.douthwaite.io"))
