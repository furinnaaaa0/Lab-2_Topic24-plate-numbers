from pathlib import Path
from urllib.parse import urlparse

import requests

class SourceError(Exception):
    # Ошибка при получении текста из источника
    pass

# Загружает текст из локального файла
def load_text_file(file_path):
    try:
        path = Path(file_path)

        if not path.is_file():
            raise SourceError("Указанный файл не найден.")

        return path.read_text(
            encoding="utf-8",
            errors="replace"
        )

    except OSError as error:
        raise SourceError(f"Не удалось прочитать файл: {error}")

# Загружает содержимое веб-страницы
def load_web_page(url):
    if not isinstance(url, str) or not url.strip():
        raise SourceError("Введите адрес веб-страницы.")

    parsed_url = urlparse(url)

    if parsed_url.scheme not in ("http", "https") or not parsed_url.netloc:
        raise SourceError("Укажите корректный URL с http:// или https://")

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        response.raise_for_status()
        response.encoding = response.apparent_encoding

        return response.text

    except requests.RequestException as error:
        raise SourceError(f"Ошибка загрузки веб-страницы: {error}")