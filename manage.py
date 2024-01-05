import settings
from src.common.feeds import load_feed_configs
from src.commands.feeds import create_or_update_feed, get_feed

feeds = load_feed_configs(settings)

for name, config in feeds.items():
    create_or_update_feed(
        name, config, settings.POST_REPOSITORY, settings.FEED_REPOSITORY
    )

print(get_feed("firehose", settings.FEED_REPOSITORY))
