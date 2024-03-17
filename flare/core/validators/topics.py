def mentions_machine_learning(
    item: ExtractedItem,
    min_term_count: int = 2,
    keywords: List[str] = MACHINE_LEARNING_KEYWORDS,
):
    counts = count_unique_hits(item.content.text.lower(), keywords)
    if counts >= min_term_count:
        return True
    else:
        return False
