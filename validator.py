import re

letters = "АВЕКМНОРСТУХABEKMHOPCTYX"

plate_pattern = re.compile(
    rf"[{letters}][0-9]{{3}}[{letters}]{{2}}[0-9]{{2,3}}"
)

# Удаляет пробелы и приводит буквы к верхнему регистру
def normalize_plate(plate):
    return re.sub(r"\s+", "", plate).upper()

# Проверяет соответствие номера установленному формату
def is_valid_plate(plate):
    if not isinstance(plate, str):
        return False

    normalized = normalize_plate(plate)

    return bool(plate_pattern.fullmatch(normalized))
