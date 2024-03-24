import pytest
from datetime import datetime
from flare.core.models.links import RichLink, LinkText, LinkImage
from flare.core.errors import RichLinkRepositoryWriteError
from flare.db.links.sqlite import SQLRichLinkRepository


@pytest.fixture
def sample_rich_link():
    return RichLink(
        id="0",
        url="https://some.url",
        title="my title",
        description="my description",
        image=LinkImage(url="https://my.cdn.com/image"),
        metadata={},
        locale="en-US",
        excerpt="a summary of my link",
        read_time=5.0,
        readability=40.0,
        tags=["example-tag"],
        attributes={"attr-1": 100, "attr-2": 222},
        featured=False,
        available=True,
        index_date="2024-03-01",
        created_at=datetime.now(),
        updated_at=None,
    )


@pytest.fixture
def rich_link_repo():
    return SQLRichLinkRepository("sqlite:///:memory:")


@pytest.fixture
def seeded_rich_link_repo(rich_link_repo, sample_rich_link):
    print("sample", sample_rich_link)
    rich_link_repo.insert(sample_rich_link)
    yield rich_link_repo


def test_insert_rich_link_succeeds(sample_rich_link, rich_link_repo):
    rich_link_repo.insert(sample_rich_link)


def test_get_rich_link_succeeds(sample_rich_link, seeded_rich_link_repo):
    retrieved_rich_link = seeded_rich_link_repo.get(sample_rich_link.id)
    assert retrieved_rich_link == sample_rich_link


def test_insert_duplicate_rich_link_fails(sample_rich_link, rich_link_repo):
    rich_link_repo.insert(sample_rich_link)

    with pytest.raises(RichLinkRepositoryWriteError):
        rich_link_repo.insert(sample_rich_link)
