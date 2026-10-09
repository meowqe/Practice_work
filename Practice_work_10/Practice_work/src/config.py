"""Конфигурация учебной ОС."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "os.sqlite"
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "os.log"

OS_NAME = "MyOS"
OS_VERSION = "0.1"

SYSCALL_TIME_LIMIT_MS = 50   # NFR: максимум на один системный вызов
MAX_PROCESSES = 10           # NFR: одновременно поддерживаемых процессов
