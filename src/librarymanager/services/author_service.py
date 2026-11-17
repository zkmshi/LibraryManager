from src.librarymanager.models.author import Author
from src.librarymanager.repositories import author_repository, book_author_repository


def create_author(first_name: str, last_name: str, middle_name: str | None):
    if not first_name.strip():
        raise ValueError("Имя не может быть пустым")

    if not last_name.strip():
        raise ValueError("Фамилия не может быть пустой")

    for a in author_repository.get_all():
        if (
            a.first_name.lower() == first_name.strip().lower()
            and a.last_name.lower() == last_name.strip().lower()
            and (a.middle_name or "").lower() == (middle_name or "").strip().lower()
        ):
            raise ValueError("Такой автор уже существует")

    author_repository.create(
        first_name.strip(), last_name.strip(), (middle_name or "").strip() or None
    )


def get_all_authors() -> list[Author]:
    return author_repository.get_all()


def get_author_by_id(author_id: int) -> Author | None:
    return author_repository.get_by_id(author_id)


def delete_author(author_id: int):
    if not author_repository.get_by_id(author_id):
        raise ValueError("Автор не найден")

    if book_author_repository.get_books_by_author(author_id):
        raise ValueError("Нельзя удалить автора: за ним числятся произведения")

    author_repository.delete(author_id)
