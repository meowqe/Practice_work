"""Системные вызовы и их журналирование в таблицу syscalls_log."""
import functools
import time

from src import db
from src.config import MAX_SYSCALL_MS


def log_syscall(name: str, args, user: str, status: str) -> None:
    """Записывает обращение к ядру в журнал."""
    conn = db.get_connection()
    try:
        conn.execute(
            "INSERT INTO syscalls_log (name, args, user, status) VALUES (?,?,?,?)",
            (name, repr(args), user, status))
        conn.commit()
    finally:
        conn.close()


def syscall(func):
    """Декоратор: автоматическое логирование, перехват ошибок, замер времени."""
    @functools.wraps(func)
    def wrapper(*args, user: str = "system", **kwargs):
        start = time.perf_counter()
        status = "OK"
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as exc:          # ядро не должно падать
            status = f"ERROR: {exc}"
        ms = (time.perf_counter() - start) * 1000
        if ms > MAX_SYSCALL_MS:
            status += f" (SLOW {ms:.1f} ms)"
        log_syscall(func.__name__, (args, kwargs), user, status)
        return result
    return wrapper


@syscall
def sys_echo(message: str) -> str:
    return message


@syscall
def sys_get_users() -> list:
    conn = db.get_connection()
    try:
        rows = conn.execute(
            "SELECT id, login, role, created_at FROM users ORDER BY id").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
