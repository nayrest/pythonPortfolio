# Python Portfolio

Портфолио учебных и pet-проектов на Python.

## Проекты

| Проект | Описание | Стек |
|--------|----------|------|
| [news_api](news_api/) | REST API: парсит новости с сайта, сохраняет в БД, отдаёт с фильтрацией, сортировкой и пагинацией, строит графики | FastAPI, SQLAlchemy, SQLite, BeautifulSoup, requests, matplotlib |
| [todo_list](todo_list/) | CRUD API для списка задач | FastAPI, SQLAlchemy, SQLite, Pydantic |
| [games/snake](games/snake/) | «Змейка» с тремя уровнями сложности, бонусной едой, препятствиями, звуками и сохранением рекорда | Python, Pygame |

### news_api
- `POST /news/parse` — парсинг сайта (по умолчанию из `config.py`, либо по параметру `url`) и сохранение в SQLite
- `GET /news`, `GET /news/{id}` — список с пагинацией и получение по ID
- `GET /news/search` — фильтры по источнику и датам, сортировка
- `GET /news/plot`, `/news/plot/date`, `/news/plot/source` — графики (PNG); `GET /news/top_words` — частые слова
- Документация Swagger: `/docs`

### todo_list
- Создание, чтение, обновление и удаление задач (`/todos/`)
- Разделение на слои: роуты, модели SQLAlchemy, схемы Pydantic, подключение к БД

### games/snake
- Управление стрелками, пауза на `P`
- Модульная структура: игровой цикл, сущности (змейка, еда, препятствия), настройки, звуки

## Быстрый старт

```bash
git clone https://github.com/nayrest/pythonPortfolio.git
cd pythonPortfolio

# API-проекты
cd news_api        # или todo_list
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Подробные инструкции по запуску — в README внутри каждой папки.
