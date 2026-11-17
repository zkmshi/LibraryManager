from src.librarymanager.database.database import get_connection
from src.librarymanager.models.role import Role


def get_all() -> list[Role]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT role_id, name FROM roles ORDER BY role_id"
    ).fetchall()
    conn.close()
    return [Role(*row) for row in rows]


def get_by_id(role_id: int) -> Role | None:
    conn = get_connection()
    row = conn.execute(
        "SELECT role_id, name FROM roles WHERE role_id = ?", (role_id,)
    ).fetchone()
    conn.close()
    return Role(*row) if row else None
