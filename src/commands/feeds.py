from src.entities.feeds import Feed, FeedBuildConfig
from src.interfaces.feeds import FeedRepository
from src.interfaces import PostRepository


def get_feed(name: str, feed_repo: FeedRepository) -> Feed:
    return feed_repo.get(name)


def create_or_update_feed(
    name: str,
    build_config: FeedBuildConfig,
    posts_repo: PostRepository,
    feeds_repo: FeedRepository,
):
    feed = build_config.builder(
        name, build_config.args, build_config.kwargs, posts_repo
    )

    if feeds_repo.exists(name):
        feeds_repo.update(name, feed)
    else:
        feeds_repo.create(name, feed)
