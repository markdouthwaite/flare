import re
import string
from typing import List, Union

from bs4 import BeautifulSoup
from nltk.tokenize import TreebankWordTokenizer


def html_parser(content: Union[str, bytes], **kwargs):
    soup = BeautifulSoup(content, "html.parser")
    return soup, *DefaultHTMLParser().text_from_soup(soup, **kwargs)


class DefaultHTMLParser:
    _URL_PATTERN = (
        r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)"
        r"(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+"
        r"(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)"
        r"|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    )

    def __init__(self):
        self._tokenizer = TreebankWordTokenizer()

    def _urls(self, s: str) -> List[str]:
        return [_[0] for _ in re.findall(self._URL_PATTERN, s)]

    def _soup(self, content: bytes) -> str:
        return BeautifulSoup(content, "html.parser").text.strip()

    def _mask_urls(self, s: str):
        return re.sub(self._URL_PATTERN, "", s)

    def text(self, content: bytes, **kwargs):
        return self.text_from_soup(BeautifulSoup(content, "html.parser"), **kwargs)

    def text_from_soup(
        self, soup: BeautifulSoup, return_urls: bool = True, mask_urls: bool = True
    ):
        raw = soup.text.strip()

        if return_urls:
            urls = self._urls(raw)

        if mask_urls:
            raw = self._mask_urls(raw)

        raw = raw.replace("`", "")
        tokens = self._tokenizer.tokenize(raw)
        tokens = (_ for _ in tokens if _ not in string.punctuation)
        tokens = (_.replace("'", "") for _ in tokens)
        tokens = (_.replace("`", "") for _ in tokens)
        cleaned = " ".join(_ for _ in tokens)

        if return_urls:
            return cleaned, urls
        else:
            return cleaned
