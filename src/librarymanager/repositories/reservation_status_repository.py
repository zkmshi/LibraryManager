from src.librarymanager.database.database import get_connection
from src.librarymanager.models.reservation_status import ReservationStatus


def get_all() -> list[ReservationStatus]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT status_id, name FROM reservation_statuses ORDER BY status_id"
    ).fetchall()
    conn.close()
    return [ReservationStatus(*row) for row in rows]


def get_by_id(status_id: int) -> ReservationStatus | None:
    conn = get_connection()
    row = conn.execute(
        "SELECT status_id, name FROM reservation_statuses WHERE status_id = ?",
        (status_id,),
    ).fetchone()
    conn.close()
    return ReservationStatus(*row) if row else None
