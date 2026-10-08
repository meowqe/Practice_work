"""Командная оболочка (пространство пользователя)."""
from src.config import OS_NAME, OS_VERSION
from src.kernel import Kernel
from src import syscalls

BANNER = f"""\
=====================================
  {OS_NAME} v{OS_VERSION} — учебная ОС
  Введите 'help' для справки
====================================="""

HELP = """Команды:
  help          — справка
  echo <текст>  — вывести текст (sys_echo)
  users         — список пользователей (sys_get_users)
  exit          — выход"""


def run(kernel=None) -> None:
    kernel = kernel or Kernel()
    print(BANNER)
    while True:
        try:
            line = input(f"{kernel.current_user}@{OS_NAME}> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        cmd, _, arg = line.partition(" ")
        if cmd == "help":
            print(HELP)
        elif cmd == "echo":
            print(syscalls.sys_echo(arg, user=kernel.current_user))
        elif cmd == "users":
            for u in syscalls.sys_get_users(user=kernel.current_user) or []:
                print(f"{u['id']:>3}  {u['login']:<10} {u['role']:<6} {u['created_at']}")
        elif cmd == "exit":
            print("Завершение работы.")
            break
        else:
            print(f"Неизвестная команда: {cmd}. Введите 'help'.")


if __name__ == "__main__":
    run()
