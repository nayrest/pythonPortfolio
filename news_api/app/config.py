from pathlib import Path
import os

# Корень проекта — папка выше модуля app
BASE_DIR = Path(__file__).resolve().parent.parent

# Путь к sqlite-файлу (works on Windows and Linux)
DB_DIR = BASE_DIR / "data"
DB_DIR.mkdir(exist_ok=True)
SQLITE_PATH = DB_DIR / "news.db"

# Полная SQLAlchemy URL строка
DATABASE_URL = f"sqlite:///{SQLITE_PATH}"

# Пример целевого URL для парсера — поменяйте под ваш сайт
# Рекомендация: используйте сайт, разрешающий парсинг (или RSS).
TARGET_URL = "https://lenta.ru"  # <- замените на реальный сайт/страницу

# User-Agent для запросов
REQUESTS_HEADERS = {
    "User-Agent": "news-api-bot/1.0 (+https://github.com/nayrest)"
}

# Настройки для графика
PLOT_TMP = DB_DIR / "plot.png"

# Linux-специфические альтернативные пути (закомментированы)
# LINUX_DB = Path("/var") / "opt" / "news_api" / "news.db"
# If you want to use Linux path, set DATABASE_URL accordingly:
# DATABASE_URL = f"sqlite:///{LINUX_DB}"
