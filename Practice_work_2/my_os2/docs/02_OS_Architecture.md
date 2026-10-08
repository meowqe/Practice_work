# Архитектура ОС

## 1. Состав модулей

- shell.py - командная оболочка, читает команды пользователя
- syscalls.py - системные вызовы, интерфейс между оболочкой и ядром
- kernel.py - ядро, обрабатывает вызовы и координирует подсистемы
- scheduler.py - планировщик, управляет процессами
- memory.py - управление памятью
- fs.py - файловая система, работает с файлами
- auth.py - аутентификация и права доступа
- db.py - работа с SQLite

Направления вызовов (только сверху вниз):

- shell.py → syscalls.py → kernel.py
- kernel.py → scheduler.py, memory.py, fs.py, auth.py
- scheduler.py, memory.py, fs.py, auth.py → db.py

Диаграмма: `docs/02_component_diagram.png`

Статус реализации: shell.py, syscalls.py, kernel.py, db.py уже есть; scheduler.py, memory.py, fs.py, auth.py пока только спроектированы (на этом занятии вызовы реализованы заглушками).

## 2. Системные вызовы

```
sys_login(login: str, password: str) -> bool
sys_logout() -> bool
sys_whoami() -> str
sys_create_file(path: str, content: str) -> int
sys_read_file(path: str) -> str
sys_delete_file(path: str) -> bool
sys_list_files(path: str) -> list
sys_exec(name: str) -> int
sys_ps() -> list
sys_kill(pid: int) -> bool
sys_mem_alloc(size: int) -> int
sys_logs(limit: int) -> list
sys_shutdown() -> bool
```

Уже реализованные на прошлом занятии: `sys_echo(message: str) -> str`, `sys_get_users() -> list`.

### Контракты

**sys_login**
- Предварительное условие: пользователь с таким логином есть в базе.
- Постусловие: возвращено True или False.
- Побочный эффект: запись в журнал syscalls_log.

**sys_create_file**
- Предварительное условие: пользователь авторизован.
- Постусловие: файл создан, возвращён его id.
- Побочный эффект: запись в syscalls_log.

**sys_kill**
- Предварительное условие: процесс с таким pid существует, у пользователя есть право его завершить.
- Постусловие: процесс завершён, возвращено True; если процесса нет - False.
- Побочный эффект: состояние процесса в таблице processes стало 'terminated', запись в syscalls_log.

## 3. Структуры данных

Поля совпадают со столбцами таблиц из src/db.py.

```python
process = {
    'pid': 1,
    'name': 'shell',
    'state': 'running',
    'owner': 'admin',
    'memory_kb': 120,
    'created_at': '2025-01-01 10:00:00'
}

file = {
    'id': 1,
    'path': '/home/test.txt',
    'content': 'hello',
    'owner': 'admin',
    'created_at': '2025-01-01 10:00:00'
}

user = {
    'id': 1,
    'login': 'admin',
    'password_hash': 'abc123...',
    'role': 'admin'
}

log = {
    'id': 1,
    'name': 'sys_login',
    'args': "('admin',)",
    'user': 'admin',
    'status': 'OK',
    'timestamp': '2025-01-01 10:00:00'
}
```
