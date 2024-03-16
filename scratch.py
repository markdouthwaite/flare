from flare.core.models.links import Link
from flare.core.extractors import arxiv, html, github


data = html.extract(
    Link(url="https://mark.douthwaite.io/a-gentle-introduction-to-retrieval-augmented-generation/"),
    {"max_chars": 5*1500})

print(data)
data = arxiv.extract(
    Link(url="https://arxiv.org/abs/1606.06565"), {"max_chars": 5*300}
)
print(data)
data = github.extract(
    Link(url="https://github.com/markdouthwaite/xanthus"), {}
)

print(data)
