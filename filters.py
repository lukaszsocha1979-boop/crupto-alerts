from config import KEYWORDS


def is_interesting(text):
    text = text.lower()

    for words in KEYWORDS.values():
        for word in words:
            if word.lower() in text:
                return True

    return False
