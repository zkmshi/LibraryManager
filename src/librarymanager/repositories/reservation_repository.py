from src.librarymanager.database.database import get_connection
from src.librarymanager.models.reservation import Reservation

ACTIVE = 1
RETURNED = 2
CANCELED = 3

_COLUMNS = (
    "reservation_id, librarian_id, reader_id, book_id, reserved_at, status_id"
)


def create(reader_id: int, book_id: int) -> int:
    conn = get_connection()
    cur = conn.execute(
        """
        INSERT INTO reservations (librarian_id, reader_id, book_id,
                                  reserved_at, status_id)
        VALUES (NULL, ?, ?, datetime('now'), ?)
        """,
        (reader_id, book_id, ACTIVE),
    )
    conn.commit()
    reservation_id = cur.lastrowid
    conn.close()
    return reservation_id


def get_by_id(reservation_id: int) -> Reservation | None:
    conn = get_connection()
    row = conn.execute(
        f"SELECT {_COLUMNS} FROM reservations WHERE reservation_id = ?",
        (reservation_id,),
    ).fetchone()
    conn.close()
    return Reservation(*row) if row else None


def get_all() -> list[Reservation]:
    conn = get_connection()
    rows = conn.execute(
        f"SELECT {_COLUMNS} FROM reservations ORDER BY reserved_at DESC"
    ).fetchall()
    conn.close()
    return [Reservation(*row) for row in rows]


def get_by_reader(reader_id: int) -> list[Reservation]:
    conn = get_connection()
    rows = conn.execute(
        f"""
        SELECT {_COLUMNS} FROM reservations
        WHERE reader_id = ? ORDER BY reserved_at DESC
        """,
        (reader_id,),
    ).fetchall()
    conn.close()
    return [Reservation(*row) for row in rows]


def get_active_by_book(book_id: int) -> Reservation | None:
    conn = get_connection()
    row = conn.execute(
        f"SELECT {_COLUMNS} FROM reservations WHERE book_id = ? AND status_id = ?",
        (book_id, ACTIVE),
    ).fetchone()
    conn.close()
    return Reservation(*row) if row else None


def has_any_by_book(book_id: int) -> bool:
    conn = get_connection()
    row = conn.execute(
        "SELECT 1 FROM reservations WHERE book_id = ? LIMIT 1", (book_id,)
    ).fetchone()
    conn.close()
    return row is not None


def mark_returned(reservation_id: int, librarian_id: int) -> None:
    conn = get_connection()
    conn.execute(
        "UPDATE reservations SET status_id = ?, librarian_id = ? WHERE reservation_id = ?",
        (RETURNED, librarian_id, reservation_id),
    )
    conn.commit()
    conn.close()


def cancel(reservation_id: int) -> None:
    conn = get_connection()
    conn.execute(
        "UPDATE reservations SET status_id = ? WHERE reservation_id = ?",
        (CANCELED, reservation_id),
    )
    conn.commit()
    conn.close()
