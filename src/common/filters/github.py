from datetime import datetime
from src.entities import Post


def is_popular_repo(post: Post, min_stars: int = 25) -> bool:
    if post.metadata.get("stars", 0) < min_stars:
        return False
    else:
        return True


def is_not_malware_repo(post: Post) -> bool:
    toxic_terms = [
        "utorrent",
        "cheat",
        "undetected",
        "spoofer",
        "aimbot",
        "hack",
        "crack",
        "injector",
        "privatecheat",
        "cheats",
        "controlnet",
        "xanthus",
        "activator",
    ]
    if any(term in post.title for term in toxic_terms):
        return False
    else:
        return True


def is_python_repo(post: Post) -> bool:
    if post.metadata.get("language") not in ["Python", "Jupyter Notebook"]:
        return False
    else:
        return True


def is_active_repo(post: Post, last_active_in_days: int = 90) -> bool:
    updated_at = post.metadata.get("updated_at")
    timestamp = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ")
    if (datetime.now() - timestamp).days <= last_active_in_days:
        return True
    else:
        return False
