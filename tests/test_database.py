import tempfile
import unittest
from pathlib import Path

from src.librarymanager.database import database
from src.librarymanager.services import auth_service, book_service, reservation_service


class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._old_path = database.DB_PATH
        database.DB_PATH = Path(self._tmp.name) / "test_library.db"
        database.init_db()

    def tearDown(self):
        database.DB_PATH = self._old_path
        self._tmp.cleanup()

    def test_tables_are_filled(self):
        conn = database.get_connection()
        for table in ("roles", "reservation_statuses", "users",
                      "authors", "books", "book_authors", "reservations"):
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            self.assertGreater(count, 0, table)
        self.assertEqual(conn.execute("PRAGMA foreign_key_check").fetchall(), [])
        conn.close()

    def test_default_users_can_log_in(self):
        self.assertEqual(auth_service.authenticate("admin", "admin").role_id, 2)
        self.assertEqual(auth_service.authenticate("reader", "reader").role_id, 1)
        self.assertIsNone(auth_service.authenticate("admin", "wrong"))

    def test_reservation_flow(self):
        reader = auth_service.authenticate("reader", "reader")
        admin = auth_service.authenticate("admin", "admin")

        reservation_service.create_reservation(reader.user_id, 4)
        self.assertFalse(book_service.is_book_available(4))
        with self.assertRaises(ValueError):
            reservation_service.create_reservation(reader.user_id, 4)

        active = [r for r in reservation_service.get_all_reservations()
                  if r.book_id == 4][0]
        reservation_service.return_book(active.reservation_id, admin.user_id)
        self.assertTrue(book_service.is_book_available(4))


if __name__ == "__main__":
    unittest.main()
