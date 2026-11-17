from src.librarymanager.database.database import get_connection
from src.librarymanager.models.user import User

_COLUMNS = (
    "user_id, first_name, last_name, middle_name, login, password_hash, role_id"
)


def create(first_name, last_name, middle_name, login, password_hash, role_id) -> int:
    conn = get_connection()
    cur = conn.execute(
        """
        INSERT INTO users (first_name, last_name, middle_name,
                           login, password_hash, role_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (first_name, last_name, middle_name, login, password_hash, role_id),
    )
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id


def get_by_login(login: str) -> User | None:
    conn = get_connection()
    row = conn.execute(
        f"SELECT {_COLUMNS} FROM users WHERE login = ?", (login,)
    ).fetchone()
    conn.close()
    return User(*row) if row else None


def get_by_id(user_id: int) -> User | None:
    conn = get_connection()
    row = conn.execute(
        f"SELECT {_COLUMNS} FROM users WHERE user_id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return User(*row) if row else None


def get_all() -> list[User]:
    conn = get_connection()
    rows = conn.execute(
        f"SELECT {_COLUMNS} FROM users ORDER BY last_name, first_name"
    ).fetchall()
    conn.close()
    return [User(*row) for row in rows]
