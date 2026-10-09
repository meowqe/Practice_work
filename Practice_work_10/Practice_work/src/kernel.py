"""Ядро: диспетчер системных вызовов с контролем времени и ошибок."""
import time
from src import config, db, syscalls
from src.logger import get_logger

log = get_logger()


class Kernel:
    def __init__(self):
        self.current_user = "anonymous"

    def boot(self) -> None:
        db.init_db()
        log.info("%s %s: загрузка ядра", config.OS_NAME, config.OS_VERSION)

    def call(self, name: str, *args):
        """Выполняет системный вызов; исключения не роняют ядро."""
        func = syscalls.TABLE.get(name)
        if func is None:
            return False, f"Неизвестный системный вызов: {name}"
        start = time.perf_counter()
        try:
            result = func(*args, user=self.current_user)
            return True, result
        except Exception as exc:  # ядро не должно падать
            log.error("%s: %s", name, exc)
            return False, f"Ошибка: {exc}"
        finally:
            ms = (time.perf_counter() - start) * 1000
            if ms > config.SYSCALL_TIME_LIMIT_MS:
                log.warning("%s: %.1f мс превышает лимит", name, ms)

    def shutdown(self) -> None:
        log.info("Завершение работы ядра")
        db.close_connection()
