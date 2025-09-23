# 📝 ToDo List API (FastAPI + SQLite)

Небольшой CRUD-проект на **FastAPI** и **SQLAlchemy** для управления задачами (ToDo-лист).  
Реализованы операции:
- Создание задачи
- Получение списка задач
- Получение одной задачи
- Обновление задачи
- Удаление задачи

---

## 🚀 Запуск проекта

1. Клонируйте репозиторий и установите зависимости:
   ```bash
   pip install -r requirements.txt
Или вручную:

    pip install fastapi uvicorn sqlalchemy pydantic
Запустите сервер:


    uvicorn todo_app.main:app --reload
Откройте в браузере:

Swagger UI: http://127.0.0.1:8000/docs

Redoc: http://127.0.0.1:8000/redoc

📂 Структура проекта
bash
Copy code
todo_app/
 ├── main.py        # роуты и логика API
 ├── models.py      # SQLAlchemy-модели
 ├── schemas.py     # Pydantic-схемы
 └── database.py    # подключение к базе
🔑 Эндпоинты
➕ Создать задачу

    curl -X POST "http://127.0.0.1:8000/todos/" \

    -H "Content-Type: application/json" \

    -d '{"title": "Купить молоко", "description": "Взять 2 литра"}'
📋 Получить список задач

    curl -X GET "http://127.0.0.1:8000/todos/"
🔍 Получить задачу по ID

    curl -X GET "http://127.0.0.1:8000/todos/1"
✏ Обновить задачу

    curl -X PUT "http://127.0.0.1:8000/todos/1" \

    -H "Content-Type: application/json" \

    -d '{"title": "Купить хлеб", "description": "Ржаной", "completed": true}'
❌ Удалить задачу

    curl -X DELETE "http://127.0.0.1:8000/todos/1"
📖 Пример через Swagger UI
Откройте http://127.0.0.1:8000/docs, чтобы протестировать все эндпоинты прямо в браузере.