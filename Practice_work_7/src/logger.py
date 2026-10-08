"""Файловый журнал ядра (дополняет таблицу syscalls_log)."""
import logging
from src import config


def get_logger(name: str = "myos") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        config.LOG_DIR.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(config.LOG_FILE, encoding="utf-8")
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
