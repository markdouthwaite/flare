import re

from src.entities import Source


def valid_url(url: str, source: Source) -> bool:
    for restrict_pattern in source.url_patterns.get("restrict", []):
        if re.match(restrict_pattern, url) is not None:
            return False

    allow_patterns = source.url_patterns.get("allow", [])

    if len(allow_patterns) == 0:
        return True

    if not any(re.match(p, url) is not None for p in allow_patterns):
        return False

    return True
