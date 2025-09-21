import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from urllib.parse import urljoin
from datetime import datetime
import re

from .schemas import NewsCreate
from .config import TARGET_URL, REQUESTS_HEADERS


# Паттерны дат для распознавания
DATE_PATTERNS = [
    r"\d{4}-\d{2}-\d{2}",       # 2025-09-21
    r"\d{2}\.\d{2}\.\d{4}",     # 21.09.2025
    r"\d{1,2} [а-яА-Я]+ \d{4}"  # 21 сентября 2025
]

# Список "мусорных" фраз для фильтрации ссылок
BLOCKLIST = [
    "все новости", "подробнее", "читать", "далее",
    "фоторепортаж", "выбрать регион", "архив",
    "главная", "ещё", "подписаться"
]


def extract_date(text: str) -> Optional[datetime]:
    """Пробует найти дату в тексте по регуляркам."""
    for pattern in DATE_PATTERNS:
        match = re.search(pattern, text)
        if match:
            try:
                date_str = match.group(0)
                if "-" in date_str:
                    return datetime.fromisoformat(date_str)
                elif "." in date_str:
                    return datetime.strptime(date_str, "%d.%m.%Y")
                else:
                    return datetime.strptime(date_str, "%d %B %Y")
            except Exception:
                pass
    return None


def clean_title(text: str) -> str:
    """Очистка заголовков от лишних пробелов и мусора."""
    return re.sub(r"\s+", " ", text).strip()


def looks_like_news(title: str) -> bool:
    """Фильтрация мусорных заголовков."""
    t = title.lower()
    if len(t) < 10:
        return False
    for bad in BLOCKLIST:
        if bad in t:
            return False
    return True


def parse_site(url: str = None) -> List[NewsCreate]:
    """Парсинг новостей с сайта (универсальный)."""
    target = url or TARGET_URL
    results = []
    seen = set()  # Для отслеживания дублей

    try:
        resp = requests.get(target, headers=REQUESTS_HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Основной поиск: article / section / div
        candidates = soup.find_all(["article", "section", "div"], limit=300)

        for el in candidates:
            a_tag = el.find("a", href=True)
            if not a_tag:
                continue

            title = clean_title(a_tag.get_text())
            if not looks_like_news(title):
                continue

            url_ = urljoin(target, a_tag["href"])
            if url_.startswith(("javascript:", "#")):
                continue

            # Ключ для антидубликации
            key = (title.lower(), url_)
            if key in seen:
                continue
            seen.add(key)

            summary = None
            p = el.find("p")
            if p:
                txt = p.get_text(strip=True)
                if len(txt) > 30:
                    summary = txt

            published_at = None
            time_tag = el.find("time")
            if time_tag:
                dt_attr = time_tag.get("datetime") or time_tag.get("data-time")
                if dt_attr:
                    try:
                        published_at = datetime.fromisoformat(dt_attr)
                    except Exception:
                        published_at = extract_date(dt_attr)
                if not published_at:
                    published_at = extract_date(time_tag.get_text(strip=True))
            else:
                published_at = extract_date(el.get_text(" "))

            results.append(
                NewsCreate(
                    title=title,
                    url=url_,
                    summary=summary,
                    source=target,
                    published_at=published_at,
                )
            )

        # fallback: если результатов мало
        if len(results) < 5:
            for a in soup.find_all("a", limit=100):
                t = clean_title(a.get_text())
                if not looks_like_news(t):
                    continue
                url_ = urljoin(target, a.get("href"))
                if url_.startswith(("javascript:", "#")):
                    continue

                key = (t.lower(), url_)
                if key in seen:
                    continue
                seen.add(key)

                results.append(NewsCreate(title=t, url=url_, summary=None, source=target))

        return results

    except Exception as e:
        print("Parser error:", e)
        return []
