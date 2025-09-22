from pydantic import BaseModel

class ToDoBase(BaseModel):
    title: str
    description: str | None = None

class ToDoCreate(ToDoBase):
    pass

class ToDoUpdate(ToDoBase):
    completed: bool

class ToDo(ToDoBase):
    id: int
    completed: bool

    class Config:
        from_attributes = True  # для Pydantic v2 (аналог orm_mode)
