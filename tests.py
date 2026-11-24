import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock

import requests

from validator import is_valid_plate, normalize_plate
from search import find_plates
from source_handler import load_text_file, load_web_page, SourceError

class PlateProgramTest(unittest.TestCase):

    # Создаёт временную папку и тестовый текстовый файл перед каждым тестом
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.file_path = Path(self.temp_directory.name) / "test.txt"

        self.file_path.write_text(
            "Автомобиль А123ВС77",
            encoding="utf-8"
        )

        self.addCleanup(self.temp_directory.cleanup)

    # Проверяет корректный кириллический номер
    def test_valid_cyrillic_plate(self):
        self.assertTrue(is_valid_plate("А123ВС77"))

    # Проверяет номер с трёхзначным кодом региона
    def test_valid_three_digit_region(self):
        self.assertTrue(is_valid_plate("М456ОР777"))

    # Проверяет номер с латинскими буквами
    def test_valid_latin_plate(self):
        self.assertTrue(is_valid_plate("A123BC77"))

    # Проверяет номер со смешанными алфавитами
    def test_mixed_alphabets(self):
        self.assertTrue(is_valid_plate("А123BC77"))

    # Проверяет обработку пробелов в номере
    def test_plate_with_spaces(self):
        self.assertTrue(is_valid_plate("А 123 ВС 77"))

    # Проверяет обработку строчных букв
    def test_lowercase_plate(self):
        self.assertTrue(is_valid_plate("а123вс77"))

    # Проверяет отклонение номера с неправильным количеством цифр
    def test_invalid_digit_count(self):
        self.assertFalse(is_valid_plate("А12ВС77"))

    # Проверяет отклонение недопустимых букв
    def test_invalid_letter(self):
        self.assertFalse(is_valid_plate("А123ДВ77"))

    # Проверяет отклонение региона неправильной длины
    def test_invalid_region_length(self):
        self.assertFalse(is_valid_plate("А123ВС7"))

    # Проверяет отклонение дополнительных символов
    def test_extra_characters(self):
        self.assertFalse(is_valid_plate("!А123ВС77"))

    # Проверяет обработку значения неправильного типа
    def test_non_string_plate(self):
        self.assertFalse(is_valid_plate(123456))

    # Проверяет нормализацию регистра и пробелов
    def test_normalize_plate(self):
        self.assertEqual(
            normalize_plate("а 123 вс 77"),
            "А123ВС77"
        )

    # Проверяет поиск одного номера в тексте
    def test_find_one_plate(self):
        result = find_plates("Автомобиль А123ВС77")

        self.assertEqual(result, ["А123ВС77"])

    # Проверяет поиск нескольких номеров
    def test_find_multiple_plates(self):
        result = find_plates("А123ВС77 и B456EK199")

        self.assertEqual(
            result,
            ["А123ВС77", "B456EK199"]
        )

    # Проверяет поиск номера с пробелами
    def test_find_plate_with_spaces(self):
        result = find_plates("Номер автомобиля: А 123 ВС 77")

        self.assertEqual(result, ["А123ВС77"])

    # Проверяет игнорирование некорректных номеров
    def test_ignore_invalid_plate(self):
        self.assertEqual(find_plates("А12ВС77"), [])

    # Проверяет отсутствие совпадений внутри длинной последовательности
    def test_ignore_part_of_long_sequence(self):
        self.assertEqual(find_plates("123А123ВС77789"), [])

    # Проверяет удаление повторяющихся результатов
    def test_remove_duplicates(self):
        result = find_plates("А123ВС77 и снова А123ВС77")

        self.assertEqual(result, ["А123ВС77"])

    # Проверяет поиск в пустом тексте
    def test_empty_text(self):
        self.assertEqual(find_plates(""), [])

    # Проверяет обработку значения неправильного типа при поиске
    def test_non_string_text(self):
        self.assertEqual(find_plates(123), [])

    # Проверяет чтение текстового файла
    def test_load_text_file(self):
        text = load_text_file(self.file_path)

        self.assertIn("А123ВС77", text)

    # Проверяет обработку отсутствующего файла
    def test_missing_file(self):
        missing_path = Path(self.temp_directory.name) / "missing.txt"

        with self.assertRaises(SourceError):
            load_text_file(missing_path)

    # Проверяет успешную загрузку веб-страницы
    def test_load_web_page(self):
        mock_response = Mock()
        mock_response.text = "<html>А123ВС77</html>"
        mock_response.apparent_encoding = "utf-8"

        with patch(
            "source_handler.requests.get",
            return_value=mock_response
        ):

            text = load_web_page("https://example.com")

            self.assertEqual(
                text,
                "<html>А123ВС77</html>"
            )

    # Проверяет отклонение некорректного URL
    def test_invalid_url(self):
        with self.assertRaises(SourceError):
            load_web_page("ftp://example.com")

    # Проверяет обработку пустого URL
    def test_empty_url(self):
        with self.assertRaises(SourceError):
            load_web_page("")

    # Проверяет обработку URL неправильного типа
    def test_non_string_url(self):
        with self.assertRaises(SourceError):
            load_web_page(123)

    # Проверяет обработку HTTP-ошибки
    def test_http_error(self):
        mock_response = Mock()

        mock_response.raise_for_status.side_effect = requests.HTTPError(
            "404 Not Found"
        )

        with patch(
            "source_handler.requests.get",
            return_value=mock_response
        ):

            with self.assertRaises(SourceError):
                load_web_page("https://example.com")

    # Проверяет обработку ошибки подключения
    def test_connection_error(self):
        with patch(
            "source_handler.requests.get",
            side_effect=requests.ConnectionError("Connection failed")
        ):

            with self.assertRaises(SourceError):
                load_web_page("https://example.com")

if __name__ == "__main__":
    unittest.main()