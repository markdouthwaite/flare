import math

from textstat import textstat


def read_time(text, wpm: int = 265) -> int:
    return int(math.ceil(len(text.split()) / wpm))


def readability(text) -> int:
    return int(math.ceil(textstat.flesch_reading_ease(text)))


