from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class NewsBase(BaseModel):
    title: str
    url: Optional[str] = None
    summary: Optional[str] = None
    source: Optional[str] = None
    published_at: Optional[datetime] = None

class NewsCreate(NewsBase):
    pass

class News(NewsBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
