from typing import Dict

from flare.common.feeds.firehose import firehose
from flare.entities.feeds import FeedBuildConfig


def load_feed_configs(s) -> Dict[str, FeedBuildConfig]:
    return {
        k: FeedBuildConfig(
            builder=v["builder"], args=v.get("args", ()), kwargs=v.get("kwargs", {})
        )
        for k, v in s.FEEDS.items()
    }


__all__ = ["load_feed_configs", "firehose"]