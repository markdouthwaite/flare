from flare.common.extract.errors import UrlExtractError, UrlExtractFilterException
from flare.common.extract.validate import valid_url
from flare.common.posts import to_post
from flare.entities import ExtractedItem, Post, Source
from flare.interfaces import PostRepository


def filter_item(
    item: ExtractedItem, source: Source, raise_exception: bool = True
) -> bool:
    for f in source.filters:
        if not f(item):
            if raise_exception:
                raise UrlExtractFilterException(
                    f"target url failed filter '{f.__name__}'"
                )
            else:
                return True

    return False


def load_post(post: Post, repo: PostRepository) -> None:
    repo.insert(post)


def extract_post(
    post_id: str,
    url: str,
    source: Source,
    validate_target_url: bool = True,
    filtered: bool = True,
):
    if validate_target_url and not valid_url(url, source):
        raise UrlExtractError("invalid url provided")

    extracted_item = source.extractor(url)

    if filtered and filter_item(extracted_item, source):
        raise UrlExtractError(
            "cannot load extracted post: the post failed filter checks"
        )

    post = to_post(post_id, extracted_item, source)

    return post


def existing_url(url: str, repo: PostRepository) -> bool:
    return repo.exists(url)


def extract_and_load_post(
    post_id: str,
    url: str,
    source: Source,
    repo: PostRepository,
    filtered: bool = True,
    overwrite_existing: bool = False,
    validate_target_url: bool = True,
) -> None:
    if validate_target_url and not valid_url(url, source):
        raise UrlExtractError("invalid url provided")

    if existing_url(url, repo) and not overwrite_existing:
        raise UrlExtractError("target url has already been extracted")

    extracted_item = source.extractor(url)

    if filtered and filter_item(extracted_item, source):
        raise UrlExtractError(
            "cannot load extracted post: the post failed filter checks"
        )

    post = to_post(post_id, extracted_item, source)

    try:
        load_post(post, repo)
    except ValueError as err:
        raise UrlExtractError(
            "cannot load extracted post: "
            "the post could not be loaded into the target repository"
        ) from err