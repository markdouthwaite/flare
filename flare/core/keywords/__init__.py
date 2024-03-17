def count_unique_hits(text: str, keywords: list) -> int:
    count = 0
    for keyword in keywords:
        if keyword in text:
            count += 1
    return count


def count_total_hits(text: str, keywords: list) -> int:
    tokens = [_.strip() for _ in text.lower().split()]
    counts = sum(_ in keywords for _ in tokens)
    return counts
