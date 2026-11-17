from src.librarymanager.auth import register_librarian_ui
from src.librarymanager.services import author_service, book_service, reservation_service


def _read_int(prompt: str) -> int | None:
    value = input(prompt)
    if not value.strip().lstrip("-").isdigit():
        print("Нужно ввести число")
        return None
    return int(value)


def _print_books():
    books = book_service.get_all_books()

    if not books:
        print("\nПроизведений нет")
        return

    print("\nСписок произведений:")
    for b in books:
        authors = ", ".join(a.full_name for a in book_service.get_book_authors(b.book_id))
        state = "свободно" if book_service.is_book_available(b.book_id) else "забронировано"
        print(f"{b.book_id}. {b.title} — {authors} (ISBN {b.isbn}) [{state}]")


def _print_authors():
    authors = author_service.get_all_authors()

    if not authors:
        print("\nАвторов нет")
        return

    print("\nСписок авторов:")
    for a in authors:
        print(f"{a.author_id}. {a.full_name}")


def _print_reservations(reservations):
    if not reservations:
        print("\nБронирований нет")
        return

    print("\nСписок бронирований:")
    for r in reservations:
        book = book_service.get_book_by_id(r.book_id)
        title = book.title if book else f"ID {r.book_id}"
        status = reservation_service.get_status_name(r.status_id)
        print(f"{r.reservation_id}. {title} | читатель {r.reader_id} | {r.reserved_at} | {status}")


# ---------- Меню администратора (библиотекаря) ----------
def librarian_menu(user):
    while True:
        print(f"\n===== Администратор ({user.login}) =====")
        print("1. Меню произведений")
        print("2. Меню авторов")
        print("3. Меню бронирований")
        print("4. Добавить администратора")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            books_menu()
        elif choice == "2":
            authors_menu()
        elif choice == "3":
            reservations_menu(user)
        elif choice == "4":
            register_librarian_ui()
        elif choice == "0":
            break
        else:
            print("Неверный выбор")


# ---------- Меню читателя ----------
def reader_menu(user):
    while True:
        print(f"\n===== Читатель ({user.login}) =====")
        print("1. Список произведений")
        print("2. Мои бронирования")
        print("3. Забронировать произведение")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            _print_books()
        elif choice == "2":
            _print_reservations(reservation_service.get_reader_reservations(user.user_id))
        elif choice == "3":
            _print_books()
            book_id = _read_int("ID произведения: ")
            if book_id is None:
                continue
            try:
                reservation_service.create_reservation(user.user_id, book_id)
                print("Произведение забронировано")
            except ValueError as e:
                print(f"Ошибка: {e}")
        elif choice == "0":
            break
        else:
            print("Неверный выбор")


# ---------- Авторы ----------
def authors_menu():
    while True:
        print("\n===== Авторы =====")
        print("1. Добавить")
        print("2. Показать")
        print("3. Удалить")
        print("0. Назад")

        choice = input("Выберите действие: ")

        if choice == "1":
            try:
                author_service.create_author(
                    input("Имя: "), input("Фамилия: "), input("Отчество: ")
                )
                print("Автор добавлен")
            except ValueError as e:
                print(f"Ошибка: {e}")
        elif choice == "2":
            _print_authors()
        elif choice == "3":
            author_id = _read_int("ID автора: ")
            if author_id is None:
                continue
            try:
                author_service.delete_author(author_id)
                print("Автор удалён")
            except ValueError as e:
                print(f"Ошибка: {e}")
        elif choice == "0":
            break
        else:
            print("Неверный выбор")


# ---------- Произведения ----------
def books_menu():
    while True:
        print("\n===== Произведения =====")
        print("1. Добавить")
        print("2. Показать")
        print("3. Удалить")
        print("0. Назад")

        choice = input("Выберите действие: ")

        if choice == "1":
            if not author_service.get_all_authors():
                print("\nВ системе нет авторов. Сначала добавьте автора.")
                continue

            title = input("Название: ")
            isbn = input("ISBN: ")
            _print_authors()
            ids_raw = input("\nВведите ID авторов через запятую: ")

            try:
                author_ids = [int(x) for x in ids_raw.split(",") if x.strip()]
                book_service.create_book(title, isbn, author_ids)
                print("Произведение добавлено")
            except ValueError as e:
                print(f"Ошибка: {e}")
        elif choice == "2":
            _print_books()
        elif choice == "3":
            book_id = _read_int("ID произведения: ")
            if book_id is None:
                continue
            try:
                book_service.delete_book(book_id)
                print("Произведение удалено")
            except ValueError as e:
                print(f"Ошибка: {e}")
        elif choice == "0":
            break
        else:
            print("Неверный выбор")


# ---------- Бронирования ----------
def reservations_menu(user):
    while True:
        print("\n===== Бронирования =====")
        print("1. Все бронирования")
        print("2. Принять возврат")
        print("0. Назад")

        choice = input("Выберите действие: ")

        if choice == "1":
            _print_reservations(reservation_service.get_all_reservations())
        elif choice == "2":
            reservation_id = _read_int("ID бронирования: ")
            if reservation_id is None:
                continue
            try:
                reservation_service.return_book(reservation_id, user.user_id)
                print("Возврат принят")
            except ValueError as e:
                print(f"Ошибка: {e}")
        elif choice == "0":
            break
        else:
            print("Неверный выбор")
