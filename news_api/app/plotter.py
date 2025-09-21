import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.orm import Session
from collections import Counter
import re
from sqlalchemy import func

from .crud import count_by_date
from .models import NewsItem

# --- Функции для построения графиков ---

def build_plot(dates, counts, title="График"):
    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(dates, counts, marker='o')
    ax.set_title(title)
    ax.set_xlabel("Дата")
    ax.set_ylabel("Количество")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf

def plot_news_by_date(db: Session):
    data = count_by_date(db)
    if not data:
        return None
    dates = [str(d[0]) for d in data]
    counts = [d[1] for d in data]
    return build_plot(dates, counts, title="Количество новостей по дате")

def plot_news_by_source(db: Session):
    q = db.query(NewsItem.source, func.count(NewsItem.id)).group_by(NewsItem.source).all()
    if not q:
        return None
    sources = [row[0] for row in q]
    counts = [row[1] for row in q]
    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(sources, counts, color="skyblue")
    ax.set_title("Количество новостей по источникам")
    ax.set_ylabel("Количество")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf

def top_words(db: Session, top_n: int = 5):
    news = db.query(NewsItem).all()
    text = " ".join([n.title + " " + (n.summary or "") for n in news]).lower()
    words = re.findall(r'\b\w+\b', text)
    counter = Counter(words)
    # Исключаем мусорные слова, можно добавить свой стоп-лист
    stop_words = set(["и","в","на","с","по","из","за","не","что","для","как","от","к","но","а"])
    for w in stop_words:
        counter.pop(w, None)
    return counter.most_common(top_n)

# --- API-ответ через StreamingResponse ---

def plot_response(db: Session) -> StreamingResponse:
    # Получаем количество новостей по дате
    rows = db.query(func.date(NewsItem.published_at), func.count(NewsItem.id)) \
        .group_by(func.date(NewsItem.published_at)).all()

    if not rows:
        # если нет данных — вернем пустой график
        dates, counts = [], []
    else:
        dates, counts = zip(*rows)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(dates, counts)
    ax.set_title("Количество новостей по датам")
    ax.set_xlabel("Дата")
    ax.set_ylabel("Количество")
    fig.autofmt_xdate()

    buf = BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

def plot_response_by_date(db: Session):
    buf = plot_news_by_date(db)
    if not buf:
        return JSONResponse({"error": "Нет данных для графика"}, status_code=404)
    return StreamingResponse(buf, media_type="image/png")

def plot_response_by_source(db: Session):
    buf = plot_news_by_source(db)
    if not buf:
        return JSONResponse({"error": "Нет данных для графика"}, status_code=404)
    return StreamingResponse(buf, media_type="image/png")
