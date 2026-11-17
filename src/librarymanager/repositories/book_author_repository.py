from src.librarymanager.database.database import get_connection
from src.librarymanager.models.author import Author
from src.librarymanager.models.book import Book


def create(author_id: int, book_id: int) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO book_authors (author_id, book_id) VALUES (?, ?)",
        (author_id, book_id),
    )
    conn.commit()
    conn.close()


def get_authors_by_book(book_id: int) -> list[Author]:
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT a.author_id, a.first_name, a.last_name, a.middle_name
        FROM book_authors ba
        JOIN authors a ON ba.author_id = a.author_id
        WHERE ba.book_id = ?
        """,
        (book_id,),
    ).fetchall()
    conn.close()
    return [Author(*row) for row in rows]


def get_books_by_author(author_id: int) -> list[Book]:
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT b.book_id, b.title, b.isbn
        FROM book_authors ba
        JOIN books b ON ba.book_id = b.book_id
        WHERE ba.author_id = ?
        """,
        (author_id,),
    ).fetchall()
    conn.close()
    return [Book(*row) for row in rows]


def delete_by_book(book_id: int) -> None:
    conn = get_connection()
    conn.execute("DELETE FROM book_authors WHERE book_id = ?", (book_id,))
    conn.commit()
    conn.close()


def delete_by_author(author_id: int) -> None:
    conn = get_connection()
    conn.execute("DELETE FROM book_authors WHERE author_id = ?", (author_id,))
    conn.commit()
    conn.close()
