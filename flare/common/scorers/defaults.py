from flare.entities import ExtractedItem


def identity_scorer(_: ExtractedItem, value: float = 1.0):
    return value
