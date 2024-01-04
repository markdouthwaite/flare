from celery import current_app
from src.commands.posts import extract_and_load_post as _extract_and_load_post


def extract_and_load_post(post_id: str, url: str, source_name: str):
    _extract_and_load_post(
        post_id,
        url,
        source=current_app.conf.sources[source_name],
        repo=current_app.conf.posts_repo,
    )
