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


def syscall(func=None, *, hide=()):
    """Декоратор: автоматическое логирование, перехват ошибок, замер времени.

    hide - индексы позиционных аргументов, которые не попадают в журнал
    (например, пароль).
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, user: str = "system", **kwargs):
            start = time.perf_counter()
            status = "OK"
            result = None
            try:
                result = f(*args, **kwargs)
            except Exception as exc:          # ядро не должно падать
                status = f"ERROR: {exc}"
            ms = (time.perf_counter() - start) * 1000
            if ms > MAX_SYSCALL_MS:
                status += f" (SLOW {ms:.1f} ms)"
            shown = tuple("***" if i in hide else a for i, a in enumerate(args))
            log_syscall(f.__name__, (shown, kwargs), user, status)
            return result
        return wrapper
    return decorator(func) if func is not None else decorator


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


# --- Заглушки системных вызовов (занятие 2) -------------------------------
# Каждая заглушка журналируется декоратором @syscall и возвращает
# правдоподобный результат. Реальная логика появится на следующих занятиях.

@syscall(hide=(1,))
def sys_login(login: str, password: str) -> bool:
    return True


@syscall
def sys_logout() -> bool:
    return True


@syscall
def sys_whoami(current_user: str = "guest") -> str:
    return current_user


@syscall
def sys_create_file(path: str, content: str) -> int:
    return 1


@syscall
def sys_read_file(path: str) -> str:
    return ""


@syscall
def sys_delete_file(path: str) -> bool:
    return True


@syscall
def sys_list_files(path: str) -> list:
    return []


@syscall
def sys_exec(name: str) -> int:
    return 42


@syscall
def sys_ps() -> list:
    return []


@syscall
def sys_kill(pid: int) -> bool:
    return True


@syscall
def sys_mem_alloc(size: int) -> int:
    return 1


@syscall
def sys_logs(limit: int = 10) -> list:
    return []


@syscall
def sys_shutdown() -> bool:
    return True


if __name__ == "__main__":
    db.init_db()
    print(sys_login("admin", "secret", user="guest"))
    print(sys_whoami("admin", user="admin"))
    print(sys_create_file("/test.txt", "hello", user="admin"))
    print(sys_ps(user="admin"))
