# from bs4 import BeautifulSoup
#
# with open("tests/data/html/index.html") as f:
#     raw = f.read()
#
# soup = BeautifulSoup(raw, "html.parser")
#
# print(soup.title.text)


# from flare.core.extractors import arxiv, github, html
# from flare.core.models.links import Link
#
# data = html.extract(
#     Link(
#         url="https://mark.douthwaite.io/a-gentle-introduction-to-retrieval-augmented-generation/"
#     ),
#     {"max_chars": 5 * 1500},
# )
#
# print(data)
# data = arxiv.extract(
#     Link(url="https://arxiv.org/abs/1606.06565"), {"max_chars": 5 * 300}
# )
# print(data)
# data = github.extract(Link(url="https://github.com/markdouthwaite/xanthus"), {})
#
# print(data)
