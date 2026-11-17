from src.librarymanager.services.auth_service import (
    authenticate,
    register_librarian,
    register_reader,
)


def _ask_person_data():
    first_name = input("Имя: ")
    last_name = input("Фамилия: ")
    middle_name = input("Отчество (можно пропустить): ")
    login = input("Логин: ")
    password = input("Пароль: ")
    return first_name, last_name, middle_name, login, password


def login():
    print("\n=== Авторизация ===")

    user = authenticate(input("Логин: "), input("Пароль: "))

    if not user:
        print("\nНеверный логин или пароль")
        return None

    print(f"\nДобро пожаловать, {user.first_name} {user.last_name}!")
    return user


def register():
    print("\n=== Регистрация читателя ===")

    try:
        register_reader(*_ask_person_data())
        print("\nРегистрация прошла успешно")
    except ValueError as e:
        print(f"\nОшибка: {e}")


def register_librarian_ui():
    print("\n=== Добавление администратора ===")

    try:
        register_librarian(*_ask_person_data())
        print("\nАдминистратор добавлен")
    except ValueError as e:
        print(f"\nОшибка: {e}")
