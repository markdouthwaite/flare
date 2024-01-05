from typing import Dict
from src.entities.feeds import FeedBuildConfig


def load_feed_configs(s) -> Dict[str, FeedBuildConfig]:
    return {
        k: FeedBuildConfig(
            builder=v["builder"], args=v.get("args", ()), kwargs=v.get("kwargs", {})
        )
        for k, v in s.FEEDS.items()
    }
