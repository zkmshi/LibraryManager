from src.librarymanager.models.author import Author
from src.librarymanager.models.book import Book
from src.librarymanager.repositories import (
    author_repository,
    book_author_repository,
    book_repository,
    reservation_repository,
)


def create_book(title: str, isbn: str, author_ids: list[int]):
    if not title.strip():
        raise ValueError("Название не может быть пустым")

    if not isbn.strip():
        raise ValueError("ISBN не может быть пустым")

    if not author_ids:
        raise ValueError("Нужно указать хотя бы одного автора")

    for author_id in author_ids:
        if not author_repository.get_by_id(author_id):
            raise ValueError(f"Автор с ID {author_id} не найден")

    if any(b.isbn == isbn.strip() for b in book_repository.get_all()):
        raise ValueError("Произведение с таким ISBN уже существует")

    book_id = book_repository.create(title.strip(), isbn.strip())

    for author_id in set(author_ids):
        book_author_repository.create(author_id, book_id)


def get_all_books() -> list[Book]:
    return book_repository.get_all()


def get_book_by_id(book_id: int) -> Book | None:
    return book_repository.get_by_id(book_id)


def delete_book(book_id: int):
    if not book_repository.get_by_id(book_id):
        raise ValueError("Произведение не найдено")

    if reservation_repository.has_any_by_book(book_id):
        raise ValueError("Нельзя удалить: по произведению есть бронирования")

    book_author_repository.delete_by_book(book_id)
    book_repository.delete(book_id)


def is_book_available(book_id: int) -> bool:
    return reservation_repository.get_active_by_book(book_id) is None


def get_book_authors(book_id: int) -> list[Author]:
    return book_author_repository.get_authors_by_book(book_id)
