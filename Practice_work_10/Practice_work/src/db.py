"""Работа с SQLite: соединение и инициализация базы данных."""
import hashlib
import sqlite3
import sys
from pathlib import Path

if __package__ in (None, ""):  # запуск как `python src/db.py`
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import config

_conn = None  # единственное соединение (см. риск блокировок SQLite)

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    login         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role          TEXT NOT NULL DEFAULT 'user',
    created_at    TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS processes (
    pid        INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    state      TEXT NOT NULL DEFAULT 'ready',
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
    user      TEXT,
    status    TEXT NOT NULL,
    timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def hash_password(password: str) -> str:
    """Необратимое хэширование пароля (SHA-256)."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_connection() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        config.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        _conn = sqlite3.connect(config.DB_PATH)
        _conn.row_factory = sqlite3.Row
    return _conn


def init_db() -> None:
    """Создаёт таблицы и учётные записи по умолчанию (если их нет)."""
    conn = get_connection()
    conn.executescript(SCHEMA)
    for login, pwd, role in (("admin", "admin123", "admin"),
                             ("user", "user123", "user")):
        conn.execute(
            "INSERT OR IGNORE INTO users (login, password_hash, role) "
            "VALUES (?, ?, ?)", (login, hash_password(pwd), role))
    conn.commit()


def close_connection() -> None:
    global _conn
    if _conn is not None:
        _conn.close()
        _conn = None


if __name__ == "__main__":
    init_db()
    tables = [r[0] for r in get_connection().execute(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name NOT LIKE 'sqlite_%'")]
    print(f"База создана: {config.DB_PATH}")
    print("Таблицы:", ", ".join(tables))
