import os
from functools import partial

from flare.core.embeddings import embed_text
from flare.core.extractors import html
from flare.core.links import init_rich_link_extractor
from flare.core.models.filters import ExtractedLinkFilterSet
from flare.core.models.links import Link, RichLinkConfig
from flare.db.links.supabase import SupabaseRichLinkRepository

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

rich_link_repo = SupabaseRichLinkRepository(
    url=url, key=key
)

rich_link_config = RichLinkConfig(
    summarizer=lambda _: _,
    attribute_scorers=[lambda _: ("sample", 1)],
    embedding_model=partial(embed_text, path="data/models/all-MiniLM-L6-v2"),
)

link_extractor_config = {}

rich_link_extractor = init_rich_link_extractor(
    html.extract,
    link_extractor_config,
    rich_link_config,
    rich_link_repo,
    extracted_link_filter_set=ExtractedLinkFilterSet(
        # filters=[lambda _: _.url != "https://mark.douthwaite.io"]
    ),
)

rich_link_extractor(Link(url="https://mark.douthwaite.io"))
