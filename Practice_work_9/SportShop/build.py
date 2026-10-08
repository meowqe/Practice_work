"""Скрипт локальной сборки: проверка окружения, тесты, запуск приложения."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def check_python_version():
    if sys.version_info < (3, 10):
        print("Требуется Python 3.10+")
        sys.exit(1)
    print(f"[OK] Python {sys.version_info.major}.{sys.version_info.minor}")


def install_dependencies():
    req = os.path.join(ROOT, "requirements.txt")
    if os.path.exists(req):
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", req], check=True)
    else:
        print("[OK] Внешние зависимости не требуются")


def check_data():
    if not os.path.exists(os.path.join(ROOT, "data", "products.json")):
        print("Файл данных не найден!")
        sys.exit(1)
    print("[OK] data/products.json найден")


def run_tests():
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        capture_output=True, text=True, cwd=ROOT,
    )
    print(result.stdout)
    print(result.stderr)
    if result.returncode != 0:
        print("Тесты не прошли!")
        sys.exit(1)
    print("[OK] Все тесты пройдены")


def run_app():
    result = subprocess.run([sys.executable, "main.py"], cwd=ROOT)
    if result.returncode != 0:
        print("Приложение завершилось с ошибкой!")
        sys.exit(1)


if __name__ == "__main__":
    os.chdir(ROOT)
    check_python_version()
    install_dependencies()
    check_data()
    run_tests()
    print("Сборка успешна!")
    print("--- Запуск приложения ---")
    run_app()
