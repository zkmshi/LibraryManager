from src.librarymanager.auth import login, register
from src.librarymanager.database.database import init_db
from src.librarymanager.menu import librarian_menu, reader_menu
from src.librarymanager.services.auth_service import LIBRARIAN_ROLE_ID


def main():
    init_db()

    while True:
        print("\n===== Library Manager =====")
        print("1. Вход")
        print("2. Регистрация читателя")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            user = login()
            if not user:
                continue

            if user.role_id == LIBRARIAN_ROLE_ID:
                librarian_menu(user)
            else:
                reader_menu(user)
        elif choice == "2":
            register()
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()
