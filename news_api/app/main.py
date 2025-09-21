from fastapi import FastAPI, Depends, HTTPException
from fastapi import Query
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import uvicorn
from typing import Optional
from . import models, crud, parser, plotter
from .database import SessionLocal, engine, Base
from .schemas import NewsCreate, News
from .config import TARGET_URL

# Создать все таблицы если их нет
Base.metadata.create_all(bind=engine)

app = FastAPI(title="News Parser API", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency: get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"msg": "News Parser API. POST /news/parse to parse and save."}

@app.post("/news/parse", response_model=list[News])
def parse_and_save(url: str | None = None, db: Session = Depends(get_db)):
    """
    Запустить парсер. Если url не указан, используется TARGET_URL из config.
    Возвращает добавленные записи.
    """
    parsed = parser.parse_site(url or TARGET_URL)
    added = []
    for item in parsed:
        # Защита: если нет заголовка — пропускаем
        if not item.title:
            continue
        # В реальном проекте стоит проверять дубли по URL или title
        created = crud.create_news(db, item)
        added.append(created)
    return added

@app.get("/news", response_model=list[News])
def list_news(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_news(db, skip=skip, limit=limit)

@app.get("/news/plot", response_class=StreamingResponse)
def news_plot(db: Session = Depends(get_db)):
    return plotter.plot_response(db)

@app.get("/news/plot/date", response_class=StreamingResponse)
def plot_news_date(db: Session = Depends(get_db)):
    return plotter.plot_response_by_date(db)

@app.get("/news/plot/source", response_class=StreamingResponse)
def plot_news_source(db: Session = Depends(get_db)):
    return plotter.plot_response_by_source(db)

@app.get("/news/top_words")
def get_top_words(db: Session = Depends(get_db), top_n: int = 5):
    return {"top_words": plotter.top_words(db, top_n)}


@app.get("/news/search", response_model=list[News])
def search_news(
    skip: int = 0,
    limit: int = 50,
    source: Optional[str] = None,
    from_date: Optional[datetime] = Query(None, description="Дата начала YYYY-MM-DD"),
    to_date: Optional[datetime] = Query(None, description="Дата конца YYYY-MM-DD"),
    sort_by: str = Query("published_at", description="Поле для сортировки"),
    order: str = Query("desc", description="asc или desc"),
    db: Session = Depends(get_db)
):
    """
    Поиск новостей с фильтрацией по дате, источнику и сортировкой.
    """
    items = crud.get_news_filtered(
        db=db,
        skip=skip,
        limit=limit,
        source=source,
        from_date=from_date,
        to_date=to_date,
        sort_by=sort_by,
        order=order
    )
    return items

@app.get("/news/{news_id}", response_model=News)
def get_news(news_id: int, db: Session = Depends(get_db)):
    item = crud.get_news_by_id(db, news_id)
    if not item:
        raise HTTPException(status_code=404, detail="News not found")
    return item

if __name__ == "__main__":
    # Для разработки: запустить через python -m app.main
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
