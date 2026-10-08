"""Конфигурация учебной ОС."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "os.sqlite"
LOG_DIR = BASE_DIR / "logs"

OS_NAME = "MyOS"
OS_VERSION = "0.1"

# Нефункциональные ограничения (см. docs/01_OS_Scope_and_NFR.md)
MAX_SYSCALL_MS = 50      # макс. время системного вызова, мс
MAX_PROCESSES = 10       # макс. число одновременных процессов
MEMORY_LIMIT_KB = 4096   # лимит памяти на процесс, КБ
