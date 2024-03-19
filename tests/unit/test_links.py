import pytest
from flare.core.models.links import (
    Link,
    ExtractedLink,
    LinkText,
    LinkImage,
    RichLinkConfig,
)
from flare.core.models.filters import LinkFilterSet, ExtractedLinkFilterSet
from flare.core.links import (
    domain,
    validate_link,
    validate_extracted_link,
    create_rich_link,
)


@pytest.fixture
def extracted_link():
    return ExtractedLink(
        url="https://my.example.site",
        title="My Example Site",
        description="An amazing site",
        text=LinkText(value="Some long-form text stripped from the linked resource"),
        image=LinkImage(url="https://some.cdn.com/my-image"),
        metadata={},
        tags=["example-tag"],
    )


@pytest.mark.parametrize(
    "url,expected_domain",
    [
        ("https://github.com", "github.com"),
        ("https://mark.douthwaite.io", "mark.douthwaite.io"),
    ],
)
def test_correct_domain_extracted(url, expected_domain):
    assert domain(url) == expected_domain


@pytest.mark.parametrize(
    "url,expected_state",
    [("https://github.com", True), ("https://mark.douthwaite.io", False),],
)
def test_validate_link_succeeds(url, expected_state):
    link = Link(url=url)

    filter_set = LinkFilterSet(
        filters=[lambda _: expected_state if url == _.url else ~expected_state]
    )

    assert validate_link(link, filter_set) == expected_state


@pytest.mark.parametrize(
    "filters, expected_state",
    [
        ([lambda _: _.title == "My Example Site"], True),
        (
            [
                lambda _: _.title == "My Example Site",
                lambda _: _.tags[0].name == "example-tag",
            ],
            True,
        ),
        (
            [
                lambda _: _.title == "My Example Site",
                lambda _: _.tags[0].name == "other-tag",
            ],
            False,
        ),
    ],
)
def test_validate_extracted_link_succeeds(filters, expected_state, extracted_link):
    filter_set = ExtractedLinkFilterSet(filters=filters)

    assert validate_extracted_link(extracted_link, filter_set) == expected_state


@pytest.mark.parametrize(
    "config,expected_attributes",
    [
        (
            RichLinkConfig(
                summarizer=lambda _: _,
                attribute_scorers=[
                    lambda _: ("title-score", 1.0)
                    if _.title == "My Example Site"
                    else ("title-score", 0.0)
                ],
            ),
            [("title-score", 1.0)],
        ),
    ],
)
def test_create_rich_link(extracted_link, config, expected_attributes):
    rich_link = create_rich_link(extracted_link, config)

    for attr in expected_attributes:
        assert rich_link.attributes[attr[0]] == attr[1]
