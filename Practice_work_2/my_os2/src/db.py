"""Работа с базой данных SQLite: подключение и инициализация."""
import hashlib
import sqlite3
import sys
from pathlib import Path

if __package__ in (None, ""):      # запуск как `python src/db.py`
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import config  # noqa: E402

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    login         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role          TEXT NOT NULL DEFAULT 'user' CHECK (role IN ('admin','user')),
    created_at    TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS processes (
    pid        INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    state      TEXT NOT NULL DEFAULT 'ready'
               CHECK (state IN ('new','ready','running','waiting','terminated')),
    owner      TEXT NOT NULL,
    memory_kb  INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS files (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    path       TEXT NOT NULL UNIQUE,
    content    TEXT NOT NULL DEFAULT '',
    owner      TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS syscalls_log (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT NOT NULL,
    args      TEXT,
    user      TEXT NOT NULL,
    status    TEXT NOT NULL,
    timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def hash_password(password: str) -> str:
    """SHA-256 хэш пароля (пароли в открытом виде не хранятся)."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_connection(path=None) -> sqlite3.Connection:
    """Возвращает соединение с БД; каталог создаётся при необходимости."""
    path = path or config.DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(path=None) -> None:
    """Создаёт четыре таблицы и учётные записи по умолчанию."""
    conn = get_connection(path)
    try:
        conn.executescript(SCHEMA)
        for login, pwd, role in (("admin", "admin123", "admin"),
                                 ("user", "user123", "user")):
            conn.execute(
                "INSERT OR IGNORE INTO users (login, password_hash, role) "
                "VALUES (?, ?, ?)", (login, hash_password(pwd), role))
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    print(f"База данных инициализирована: {config.DB_PATH}")
