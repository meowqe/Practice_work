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
  whoami        — текущий пользователь (sys_whoami)
  login         — войти (sys_login)
  logout        — выйти (sys_logout)
  create        — создать файл (sys_create_file)
  ls            — список файлов (sys_list_files)
  ps            — список процессов (sys_ps)
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
        user = kernel.current_user
        if cmd == "help":
            print(HELP)
        elif cmd == "echo":
            print(syscalls.sys_echo(arg, user=user))
        elif cmd == "users":
            for u in syscalls.sys_get_users(user=user) or []:
                print(f"{u['id']:>3}  {u['login']:<10} {u['role']:<6} {u['created_at']}")
        elif cmd == "whoami":
            print(syscalls.sys_whoami(user, user=user))
        elif cmd == "login":
            login = input("Логин: ")
            password = input("Пароль: ")
            if syscalls.sys_login(login, password, user=user):
                kernel.set_user(login)
                print(f"Вы вошли как {login}")
            else:
                print("Ошибка входа")
        elif cmd == "logout":
            syscalls.sys_logout(user=user)
            kernel.set_user("guest")
        elif cmd == "create":
            path = input("Путь: ")
            content = input("Содержимое: ")
            fid = syscalls.sys_create_file(path, content, user=user)
            print(f"Создан файл с id={fid}")
        elif cmd == "ls":
            for f in syscalls.sys_list_files("/", user=user) or []:
                print(f)
        elif cmd == "ps":
            for p in syscalls.sys_ps(user=user) or []:
                print(p)
        elif cmd == "exit":
            print("Завершение работы.")
            break
        else:
            print(f"Неизвестная команда: {cmd}. Введите 'help'.")


if __name__ == "__main__":
    run()
