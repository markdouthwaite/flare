from datetime import datetime
from flare.core.keywords import malware
from flare.core.models.links import ExtractedLink


def is_popular_repo(link: ExtractedLink, min_stars: int = 25) -> bool:
    if link.metadata.get("stars", 0) < min_stars:
        return False
    else:
        return True


def is_not_malware_repo(link: ExtractedLink) -> bool:
    if any(term in link.title for term in malware.KEYWORDS):
        return False
    else:
        return True


def is_python_repo(link: ExtractedLink) -> bool:
    if link.metadata.get("language") not in ["Python", "Jupyter Notebook"]:
        return False
    else:
        return True


def is_active_repo(link: ExtractedLink, last_active_in_days: int = 90) -> bool:
    updated_at = link.metadata.get("updated_at")
    timestamp = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ")
    if (datetime.now() - timestamp).days <= last_active_in_days:
        return True
    else:
        return False
