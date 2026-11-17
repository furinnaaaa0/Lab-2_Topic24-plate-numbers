from validator import is_valid_plate, normalize_plate
from search import find_plates
from source_handler import load_text_file, load_web_page, SourceError

# Выводит результаты поиска
def show_results(plates):
    if not plates:
        print("\nПодходящие номера не найдены.")
        return

    print(f"\nНайдено номеров: {len(plates)}")

    for index, plate in enumerate(plates, start=1):
        print(f"{index}. {plate}")

# Считывает текст до пустой строки
def read_multiline_text():
    print("\nВведите текст.")
    print("Для завершения ввода нажмите Enter на пустой строке.")

    lines = []

    while True:
        line = input()

        if not line:
            break

        lines.append(line)

    return "\n".join(lines)

# Запускает главное меню программы
def main():
    while True:
        print("\n===================================")
        print("     ПРОВЕРКА ГОСНОМЕРОВ РФ")
        print("===================================")
        print("1. Проверить один номер")
        print("2. Найти номера в тексте")
        print("3. Найти номера в файле")
        print("4. Найти номера на веб-странице")
        print("0. Выход")

        choice = input("\nВыберите действие: ").strip()

        if choice == "1":
            plate = input("\nВведите номер: ")

            if is_valid_plate(plate):
                print(
                    f"\nНомер {normalize_plate(plate)} "
                    "соответствует формату."
                )
            else:
                print("\nНомер не соответствует формату.")

        elif choice == "2":
            text = read_multiline_text()
            plates = find_plates(text)
            show_results(plates)

        elif choice == "3":
            file_path = input("\nВведите путь к файлу: ").strip()

            try:
                text = load_text_file(file_path)
                plates = find_plates(text)
                show_results(plates)

            except SourceError as error:
                print(f"\nОшибка: {error}")

        elif choice == "4":
            url = input("\nВведите URL веб-страницы: ").strip()

            try:
                text = load_web_page(url)
                plates = find_plates(text)
                show_results(plates)

            except SourceError as error:
                print(f"\nОшибка: {error}")

        elif choice == "0":
            print("\nРабота программы завершена.")
            break

        else:
            print("\nНеизвестная команда. Попробуйте снова.")

if __name__ == "__main__":
    main()