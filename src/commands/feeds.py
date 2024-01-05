from src.entities.feeds import Feed, FeedBuildConfig
from src.interfaces.feeds import FeedRepository
from src.interfaces import PostRepository


def get_feed(name: str, feed_repo: FeedRepository) -> Feed:
    return feed_repo.get(name)


def create_or_update_feed(
    name: str,
    build_config: FeedBuildConfig,
    post_repo: PostRepository,
    feed_repo: FeedRepository,
):
    feed = build_config.builder(name, build_config.args, build_config.kwargs, post_repo)

    if feed_repo.exists(name):
        feed_repo.update(name, feed)
    else:
        feed_repo.create(name, feed)
