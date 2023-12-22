from src.entities import Post, Source
from src.interfaces import PostRepository
from src.common.posts import to_post
from src.common.extract.validate import valid_url


def extract_post(url: str, source: Source, validate_target_url: bool = True) -> Post:
    if validate_target_url and not valid_url(url, source):
        raise ValueError("invalid url provided")

    extracted_item = source.extractor(url)
    post = to_post(extracted_item, source)
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
    url: str,
    source: Source,
    repo: PostRepository,
    filtered: bool = True,
    validate_target_url: bool = True,
) -> None:
    post = extract_post(url, source, validate_target_url=validate_target_url)

    if filtered and filter_post(post, source):
        raise ValueError("cannot load extracted post: the post failed filter checks")
    else:
        load_post(post, repo)
