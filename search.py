import re

from validator import letters

search_pattern = re.compile(
    rf"(?<![A-Za-zА-Яа-яЁё0-9])"
    rf"([{letters}])"
    rf"\s*([0-9]{{3}})"
    rf"\s*([{letters}]{{2}})"
    rf"\s*([0-9]{{2,3}})"
    rf"(?![A-Za-zА-Яа-яЁё0-9])",
    re.IGNORECASE
)

# Находит все подходящие регистрационные знаки в тексте
def find_plates(text):
    if not isinstance(text, str):
        return []

    matches = search_pattern.finditer(text)

    results = []

    for match in matches:
        plate = "".join(match.groups()).upper()
        results.append(plate)

    return results