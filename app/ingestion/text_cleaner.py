import re

def clean_text(text):
    # remove multiple spaces
    text = re.sub(r'\s+', ' ', text)

    # remove page numbers like 57, 58 etc
    text = re.sub(r'\b\d{2,3}\b', '', text)

    # remove common policy words
    remove_words = [
        "NEP",
        "policy",
        "framework",
        "guidelines for implementation"
    ]

    for word in remove_words:
        text = text.replace(word, "")

    return text.strip()
