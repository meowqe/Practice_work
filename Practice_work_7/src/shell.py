"""Командная оболочка (User Space)."""
from src import config
from src.kernel import Kernel

BANNER = f"""=========================================
  {config.OS_NAME} v{config.OS_VERSION} — учебная ОС
  Введите help для справки
========================================="""

HELP = """Команды:
  help          — справка
  echo <текст>  — вывести текст через sys_echo
  users         — список пользователей (sys_get_users)
  exit          — выход"""


def main() -> None:
    kernel = Kernel()
    kernel.boot()
    print(BANNER)
    while True:
        try:
            line = input("myos> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        cmd, _, rest = line.partition(" ")
        if cmd == "help":
            print(HELP)
        elif cmd == "echo":
            ok, res = kernel.call("sys_echo", rest)
            print(res)
        elif cmd == "users":
            ok, res = kernel.call("sys_get_users")
            if ok:
                for u in res:
                    print(f"{u['id']:>3}  {u['login']:<10} {u['role']:<6} {u['created_at']}")
            else:
                print(res)
        elif cmd == "exit":
            print("Завершение работы.")
            break
        else:
            print(f"Неизвестная команда: {cmd}. Введите help.")
    kernel.shutdown()


if __name__ == "__main__":
    main()
