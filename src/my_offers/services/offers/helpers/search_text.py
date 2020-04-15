import re
from typing import Pattern


PHONE_PATTERN: Pattern = re.compile(r'[\+\s]?[78]?\D*(\d{3})\D*(\d{3})\D*(\d{2})\D*(\d{2})')


def prepare_search_text(search_text: str) -> str:
    phones = re.search(PHONE_PATTERN, search_text)
    if not phones:
        return search_text

    for phone in re.finditer(PHONE_PATTERN, search_text):
        search_text = search_text.replace(phone.group(), ' ' + ''.join(phone.groups()))

    return search_text
