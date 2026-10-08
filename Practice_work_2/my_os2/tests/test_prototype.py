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

    def test_stubs_logged(self):
        self.assertTrue(syscalls.sys_login("admin", "secret", user="guest"))
        self.assertEqual(syscalls.sys_whoami("admin", user="admin"), "admin")
        self.assertEqual(syscalls.sys_create_file("/t.txt", "hi", user="admin"), 1)
        self.assertEqual(syscalls.sys_ps(user="admin"), [])
        self.assertEqual(syscalls.sys_exec("x", user="admin"), 42)
        self.assertEqual(syscalls.sys_read_file("/t.txt", user="admin"), "")
        c = db.get_connection()
        rows = c.execute("SELECT name, args FROM syscalls_log").fetchall()
        names = [r[0] for r in rows]
        for n in ("sys_login", "sys_whoami", "sys_create_file", "sys_ps"):
            self.assertIn(n, names)

    def test_password_not_logged(self):
        syscalls.sys_login("admin", "secret", user="guest")
        c = db.get_connection()
        args = c.execute("SELECT args FROM syscalls_log WHERE name='sys_login'").fetchone()[0]
        self.assertNotIn("secret", args)


if __name__ == "__main__":
    unittest.main()
