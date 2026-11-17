import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_PATH = PROJECT_ROOT / "library.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    if DB_PATH.exists():
        return

    sql_script = SCHEMA_PATH.read_text(encoding="utf-8")

    conn = get_connection()
    try:
        conn.executescript(sql_script)
        conn.commit()
    finally:
        conn.close()

    print("База данных создана.")
