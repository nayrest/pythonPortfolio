# News Parser API

Универсальный парсер новостей на Python с FastAPI.  
Поддерживает:  
- Парсинг любых новостных сайтов  
- Сбор заголовков, ссылок, краткого описания и даты публикации  
- Фильтрацию и сортировку через API  
- Визуализацию данных через графики  

---

## Установка

1. Клонировать репозиторий:
git clone https://github.com/nayrest/pythonPortfolio.git
cd news_api
Создать виртуальное окружение и активировать его:

python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / Mac
source .venv/bin/activate
Установить зависимости:

pip install -r requirements.txt
Установить Playwright и браузеры (для рендеринга JS):

Настройка:
Настройки находятся в config.py:
TARGET_URL = "https://lenta.ru/"
REQUESTS_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
Запуск
python -m app.main
API будет доступно по адресу:
http://127.0.0.1:8000

Эндпоинты API
Главная
GET /
Возвращает сообщение о работе API.

Парсинг и сохранение новостей:
POST /news/parse
Параметры:

url (опционально) — сайт для парсинга. Если не указан, берется TARGET_URL.

Список новостей:
GET /news
Параметры:

skip — пропустить N записей

limit — максимальное количество записей

Новости по ID
GET /news/{news_id}
Поиск новостей
GET /news/search
Параметры:

skip, limit — пагинация

source — фильтр по сайту

from_date, to_date — фильтр по дате (YYYY-MM-DD)

sort_by — поле для сортировки (published_at по умолчанию)

order — asc или desc

Графики новостей
GET /news/plot
Возвращает график (StreamingResponse) для визуализации количества новостей по датам.

Примеры использования
Curl
Получить последние новости:

curl -X GET "http://127.0.0.1:8000/news?skip=0&limit=10" -H "accept: application/json"
Парсинг новостей с указанного сайта:

curl -X POST "http://127.0.0.1:8000/news/parse?url=https://wylsa.com/category/news/" -H "accept: application/json"
Поиск новостей по источнику и дате:

curl -X GET "http://127.0.0.1:8000/news/search?source=https://wylsa.com&from_date=2025-09-01&to_date=2025-09-30&sort_by=published_at&order=desc" -H "accept: application/json"
Swagger UI
FastAPI автоматически предоставляет документацию и тестирование API через Swagger UI:
http://127.0.0.1:8000/docs

Здесь можно:

Просматривать все эндпоинты

Вводить параметры

Отправлять запросы и смотреть ответы прямо из браузера

Примечания

Парсер универсальный, но на некоторых сайтах сложная структура может требовать дополнительной настройки.