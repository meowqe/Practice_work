import unittest
import tempfile
from pathlib import Path
from src import config, db
from src.kernel import Kernel


class SmokeTest(unittest.TestCase):
    def setUp(self):
        db.close_connection()
        self._orig = config.DB_PATH
        self._tmp = tempfile.TemporaryDirectory()
        config.DB_PATH = Path(self._tmp.name) / "t.sqlite"

    def tearDown(self):
        db.close_connection()
        config.DB_PATH = self._orig
        self._tmp.cleanup()

    def test_boot_and_logging(self):
        k = Kernel(); k.boot()
        self.assertEqual(k.call("sys_echo", "hi"), (True, "hi"))
        ok, users = k.call("sys_get_users")
        self.assertTrue(ok)
        self.assertEqual({u["login"] for u in users}, {"admin", "user"})
        names = [r[0] for r in db.get_connection().execute("SELECT name FROM syscalls_log")]
        self.assertEqual(names, ["sys_echo", "sys_get_users"])
        self.assertFalse(k.call("nope")[0])
        k.shutdown()

    def test_passwords_hashed(self):
        db.init_db()
        h = db.get_connection().execute(
            "SELECT password_hash FROM users WHERE login='admin'").fetchone()[0]
        self.assertEqual(h, db.hash_password("admin123"))
        self.assertEqual(len(h), 64)


if __name__ == "__main__":
    unittest.main()
