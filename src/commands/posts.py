from src.entities import Post, Source
from src.interfaces import PostRepository
from src.common.posts import to_post
from src.common.extract.errors import UrlExtractError
from src.common.extract.validate import valid_url


def extract_post(post_id: str, url: str, source: Source) -> Post:
    extracted_item = source.extractor(url)
    post = to_post(post_id, extracted_item, source)
    return post


def filter_post(post: Post, source: Source) -> bool:
    for f in source.filters:
        if not f(post):
            print(f)
            return True

    return False


def load_post(post: Post, repo: PostRepository) -> None:
    repo.insert(post)


def extract_and_load_post(
    post_id: str,
    url: str,
    source: Source,
    repo: PostRepository,
    filtered: bool = True,
    validate_target_url: bool = True,
) -> None:
    if validate_target_url and not valid_url(url, source):
        raise UrlExtractError("invalid url provided")

    post = extract_post(post_id, url, source)

    if filtered and filter_post(post, source):
        raise UrlExtractError(
            "cannot load extracted post: the post failed filter checks"
        )
    else:
        try:
            load_post(post, repo)
        except ValueError:
            raise UrlExtractError(
                "cannot load extracted post: "
                "the post could not be loaded into the target repository"
            )
