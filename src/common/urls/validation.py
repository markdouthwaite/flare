from src.common.errors.url_validation import InvalidUrl


UNSUPPORTED_DOMAINS = (
    "https://twitter.com",
    "https://youtube.com",
    "https://facebook.com",
    "https://instagram.com",
)


def check_url(url: str) -> bool:
    if url.startswith(UNSUPPORTED_DOMAINS):
        raise InvalidUrl("unsupported domain")
    if not url.startswith("http"):
        raise InvalidUrl("invalid url schema")

    return True
