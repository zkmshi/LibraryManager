from src.librarymanager.database.database import get_connection
from src.librarymanager.models.author import Author

_COLUMNS = "author_id, first_name, last_name, middle_name"


def create(first_name: str, last_name: str, middle_name: str | None) -> int:
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO authors (first_name, last_name, middle_name) VALUES (?, ?, ?)",
        (first_name, last_name, middle_name),
    )
    conn.commit()
    author_id = cur.lastrowid
    conn.close()
    return author_id


def get_by_id(author_id: int) -> Author | None:
    conn = get_connection()
    row = conn.execute(
        f"SELECT {_COLUMNS} FROM authors WHERE author_id = ?", (author_id,)
    ).fetchone()
    conn.close()
    return Author(*row) if row else None


def get_all() -> list[Author]:
    conn = get_connection()
    rows = conn.execute(
        f"SELECT {_COLUMNS} FROM authors ORDER BY last_name, first_name"
    ).fetchall()
    conn.close()
    return [Author(*row) for row in rows]


def delete(author_id: int) -> None:
    conn = get_connection()
    conn.execute("DELETE FROM authors WHERE author_id = ?", (author_id,))
    conn.commit()
    conn.close()
