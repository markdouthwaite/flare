import pytest
from unittest.mock import patch

from flare.core.models.links import Link
from flare.core.extractors import github, arxiv, html


@patch("flare.core.extractors.common.requests.get")
def test_arxiv_extractor_succeeds(mock_get, sample_arxiv_html):
    mock_get.return_value.content = sample_arxiv_html
    max_chars = 5 * 300
    url = "https://arxiv.org/abs/2312.09857"
    extracted_link = arxiv.extract(Link(url=url), {"max_chars": max_chars})

    assert extracted_link.url == url
    assert (
        extracted_link.title
        == "Deep Unsupervised Domain Adaptation for Time Series Classification: "
        "a Benchmark"
    )
    assert len(extracted_link.text.value) <= max_chars
    assert len(extracted_link.description) <= max_chars
    assert len(extracted_link.metadata["authors"]) == 5


@patch("flare.core.extractors.common.requests.get")
def test_html_extractor_succeeds(mock_get, sample_html):
    mock_get.return_value.content = sample_html
    max_chars = 5 * 300
    url = "https://my.example.com"
    extracted_link = html.extract(Link(url=url), {"max_chars": max_chars})

    assert extracted_link.url == url
    assert extracted_link.title == "My Demo Site"
    assert len(extracted_link.text.value) <= max_chars


@patch("flare.core.extractors.common.fetch")
@patch("flare.core.extractors.common.fetch_json")
def test_github_extractor_succeeds(
    mock_fetch,
    mock_fetch_json,
    sample_github_readme,
    sample_github_repository_api_response,
):
    mock_fetch.return_value = sample_github_readme
    mock_fetch_json.return_value = sample_github_repository_api_response
    max_chars = 5 * 1500
    url = "https://github.com/markdouthwaite/xanthus"
    extracted_link = github.extract(Link(url=url), {"max_chars": max_chars})

    assert extracted_link.url == url
    assert extracted_link.metadata["stars"] == 4
    assert extracted_link.title == "markdouthwaite/xanthus"
