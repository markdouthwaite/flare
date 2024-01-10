from datetime import datetime

from flare.entities import ExtractedItem


def is_popular_repo(item: ExtractedItem, min_stars: int = 25) -> bool:
    if item.metadata.get("stars", 0) < min_stars:
        return False
    else:
        return True


def is_not_malware_repo(item: ExtractedItem) -> bool:
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
        "activator",
    ]
    if any(term in item.content.title for term in toxic_terms):
        return False
    else:
        return True


def is_python_repo(item: ExtractedItem) -> bool:
    if item.metadata.get("language") not in ["Python", "Jupyter Notebook"]:
        return False
    else:
        return True


def is_active_repo(item: ExtractedItem, last_active_in_days: int = 90) -> bool:
    updated_at = item.metadata.get("updated_at")
    timestamp = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ")
    if (datetime.now() - timestamp).days <= last_active_in_days:
        return True
    else:
        return False
