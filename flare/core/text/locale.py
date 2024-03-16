import pycld2 as cld2


def detect(text: str) -> str:
    try:
        is_reliable, _, details = cld2.detect(text, isPlainText=True)

        if not is_reliable:
            locale = "unknown"
        elif len(details) > 0 and details[0][1] == "en":
            significant_langs = [_ for _ in details[1:] if _[2] >= 20]
            if len(significant_langs) > 0:
                locale = sorted(significant_langs, key=lambda _: -_[2])[0][1]
            else:
                locale = "en"
        else:
            locale = details[0][1]
    except (cld2.error, TypeError):
        locale = "unknown"

    return locale
