import tempfile
import unittest
from pathlib import Path

from src import config, db, syscalls


class PrototypeTest(unittest.TestCase):
    def setUp(self):
        self._orig = config.DB_PATH
        config.DB_PATH = Path(tempfile.mkdtemp()) / "t.sqlite"
        db.init_db()

    def tearDown(self):
        config.DB_PATH = self._orig

    def test_tables(self):
        c = db.get_connection()
        names = {r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertTrue({"users", "processes", "files", "syscalls_log"} <= names)

    def test_password_hashed(self):
        c = db.get_connection()
        h = c.execute("SELECT password_hash FROM users WHERE login='admin'").fetchone()[0]
        self.assertEqual(h, db.hash_password("admin123"))
        self.assertNotEqual(h, "admin123")

    def test_syscalls_logged(self):
        self.assertEqual(syscalls.sys_echo("hi", user="admin"), "hi")
        self.assertEqual(len(syscalls.sys_get_users(user="admin")), 2)
        c = db.get_connection()
        names = [r[0] for r in c.execute("SELECT name FROM syscalls_log")]
        self.assertIn("sys_echo", names)
        self.assertIn("sys_get_users", names)


if __name__ == "__main__":
    unittest.main()
