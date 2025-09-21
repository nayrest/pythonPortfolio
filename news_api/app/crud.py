from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import Optional, List
from . import models, schemas


def create_news(db: Session, news_in: schemas.NewsCreate):
    item = models.NewsItem(
        title=news_in.title,
        url=news_in.url,
        summary=news_in.summary,
        source=news_in.source,
        published_at=news_in.published_at or datetime.utcnow()
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_news(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.NewsItem).order_by(models.NewsItem.published_at.desc()).offset(skip).limit(limit).all()


def get_news_by_id(db: Session, news_id: int):
    return db.query(models.NewsItem).filter(models.NewsItem.id == news_id).first()


def count_by_date(db: Session):
    # Для SQLite: func.date() извлекает YYYY-MM-DD
    q = db.query(
        func.date(models.NewsItem.published_at).label("d"),
        func.count(models.NewsItem.id)
    ).group_by("d").order_by("d")
    return [(row[0], row[1]) for row in q.all()]


def get_news_filtered(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    source: Optional[str] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    sort_by: str = "published_at",
    order: str = "desc"
) -> List[models.NewsItem]:
    """
    Получение новостей с фильтрацией, сортировкой и пагинацией.
    """
    query = db.query(models.NewsItem)

    if source:
        query = query.filter(models.NewsItem.source == source)
    if from_date:
        query = query.filter(models.NewsItem.published_at >= from_date)
    if to_date:
        query = query.filter(models.NewsItem.published_at <= to_date)

    # Сортировка
    sort_col = getattr(models.NewsItem, sort_by, models.NewsItem.published_at)
    if order.lower() == "desc":
        sort_col = sort_col.desc()
    else:
        sort_col = sort_col.asc()

    return query.order_by(sort_col).offset(skip).limit(limit).all()
