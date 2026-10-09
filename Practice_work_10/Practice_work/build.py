"""Сборка релиза: запускает тесты и упаковывает проект в dist/SportShop-<версия>.zip."""
import os
import subprocess
import sys
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
VERSION = "1.0"
INCLUDE = ["src", "data", "docs", "main.py", "README.md"]
SKIP_DIRS = {"__pycache__"}
SKIP_FILES = {"cart.json", "orders.json"}
# Модули учебной ОС (практики 1-6) в релиз магазина не входят
SKIP_PATHS = {"kernel.py", "syscalls.py", "shell.py", "db.py", "config.py", "logger.py"}


def run_tests():
    print("Запуск тестов...")
    result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."], cwd=ROOT)
    return result.returncode == 0


def build():
    if not run_tests():
        print("Сборка прервана: тесты не прошли", file=sys.stderr)
        return 1

    dist = os.path.join(ROOT, "dist")
    os.makedirs(dist, exist_ok=True)
    archive = os.path.join(dist, f"SportShop-{VERSION}.zip")
    count = 0
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in INCLUDE:
            full = os.path.join(ROOT, item)
            if os.path.isfile(full):
                zf.write(full, item)
                count += 1
                continue
            for folder, dirs, files in os.walk(full):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for name in files:
                    if name in SKIP_FILES or name.endswith(".pyc") or (item == "src" and name in SKIP_PATHS):
                        continue
                    path = os.path.join(folder, name)
                    zf.write(path, os.path.relpath(path, ROOT))
                    count += 1
    print(f"Сборка завершена: {os.path.relpath(archive, ROOT)} ({count} файлов)")
    return 0


if __name__ == "__main__":
    sys.exit(build())
