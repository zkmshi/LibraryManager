from src.librarymanager.database.database import get_connection
from src.librarymanager.models.book import Book


def create(title: str, isbn: str) -> int:
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO books (title, isbn) VALUES (?, ?)", (title, isbn)
    )
    conn.commit()
    book_id = cur.lastrowid
    conn.close()
    return book_id


def get_by_id(book_id: int) -> Book | None:
    conn = get_connection()
    row = conn.execute(
        "SELECT book_id, title, isbn FROM books WHERE book_id = ?", (book_id,)
    ).fetchone()
    conn.close()
    return Book(*row) if row else None


def get_all() -> list[Book]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT book_id, title, isbn FROM books ORDER BY title"
    ).fetchall()
    conn.close()
    return [Book(*row) for row in rows]


def delete(book_id: int) -> None:
    conn = get_connection()
    conn.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
    conn.commit()
    conn.close()
