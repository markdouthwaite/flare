import pytest


@pytest.fixture
def sample_html():
    with open("data/html/index.html", "rb") as f:
        return f.read()


@pytest.fixture
def sample_github_readme():
    with open("data/github/readme.md", "rb") as f:
        return f.read()


@pytest.fixture
def sample_github_repository_api_response():
    with open("data/github/api/repository.json", "rb") as f:
        return f.read()


@pytest.fixture
def sample_arxiv_html():
    with open("data/arxiv/index.html", "rb") as f:
        return f.read()
