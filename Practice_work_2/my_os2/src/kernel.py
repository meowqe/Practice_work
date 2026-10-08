"""Минимальное ядро: хранит состояние текущей сессии."""
from src import db


class Kernel:
    def __init__(self):
        db.init_db()              # БД создаётся автоматически при запуске
        self.current_user = "guest"

    def set_user(self, login: str) -> None:
        self.current_user = login
