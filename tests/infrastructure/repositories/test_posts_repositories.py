import pytest
from flare.infrastructure.repositories.posts import SQLPostRepository
from flare.common.errors import PostRepositoryWriteError
from datetime import datetime
from flare.entities import Post, Tag


@pytest.fixture(scope="session")
def sample_post():
    post = Post(
        id="0",
        url="https://mark.douthwaite.io",
        kind="article",
        title="Mark Douthwaite",
        description="Personal website of Mark Douthwaite",
        text="the text of the post goes here",
        image_url=None,
        locale="en",
        excerpt="the summary of the text/post goes here",
        featured=False,
        status="available",
        readability=0,
        read_time=0,
        rating=1.0,
        metadata={
            "misc": "misc info goes here as a dictionary, should be JSON serializable"
        },
        created_at=datetime.now(),
        created_by="mark@differential.pub",
        updated_at=None,
        updated_by=None,
        tags=[
            Tag(name="demo")
        ]
    )
    return post


@pytest.fixture
def sqlite_repository(tmp_path):
    return SQLPostRepository(f"sqlite://")


@pytest.fixture
def repository(sqlite_repository):
    return sqlite_repository


def test_insert_post_succeeds(sample_post, repository):
    repository.insert(sample_post)


def test_list_posts_succeeds(sample_post, repository):
    repository.insert(sample_post)
    posts = repository.list()
    assert all(isinstance(post, Post) for post in posts)
    assert len(posts) == 1


def test_get_post_succeeds(sample_post, repository):
    repository.insert(sample_post)
    post = repository.get(sample_post.id)
    assert isinstance(post, Post)


def test_primary_key_constraint(sample_post, repository):
    repository.insert(sample_post)
    with pytest.raises(PostRepositoryWriteError):
        repository.insert(sample_post)


def test_post_exists_succeeds(sample_post, repository):
    repository.insert(sample_post)
    assert repository.exists(sample_post.url)
