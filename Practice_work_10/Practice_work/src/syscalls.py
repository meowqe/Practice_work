"""Системные вызовы. Каждый вызов автоматически журналируется."""
import functools
from src.db import get_connection
from src.logger import get_logger

log = get_logger()


def log_syscall(name: str, args, user: str, status: str) -> None:
    """Запись в таблицу syscalls_log."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO syscalls_log (name, args, user, status) "
        "VALUES (?, ?, ?, ?)", (name, repr(args), user, status))
    conn.commit()
    log.info("%s args=%r user=%s status=%s", name, args, user, status)


def syscall(func):
    """Декоратор: логирует успех (ok) или ошибку (error: ...)."""
    @functools.wraps(func)
    def wrapper(*args, user: str = "anonymous", **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as exc:
            log_syscall(func.__name__, args, user, f"error: {exc}")
            raise
        log_syscall(func.__name__, args, user, "ok")
        return result
    return wrapper


@syscall
def sys_echo(message: str) -> str:
    return message


@syscall
def sys_get_users() -> list:
    rows = get_connection().execute(
        "SELECT id, login, role, created_at FROM users ORDER BY id")
    return [dict(r) for r in rows]


TABLE = {"sys_echo": sys_echo, "sys_get_users": sys_get_users}
