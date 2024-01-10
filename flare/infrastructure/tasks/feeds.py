from celery import current_app, shared_task
from src.commands.feeds import create_or_update_feed as _create_or_update_feed


@shared_task(ignore_result=False)
def create_or_update_feed(name: str):
    build_config = current_app.conf.FEEDS[name]
    posts_repo = current_app.conf.POSTS_REPO
    feeds_repo = current_app.conf.FEEDS_REPO
    _create_or_update_feed(
        name, build_config=build_config, feeds_repo=feeds_repo, posts_repo=posts_repo
    )
