from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database

# создаем таблицы
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# зависимость: сессия базы
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в ToDo API!"}

@app.post("/todos/", response_model=schemas.ToDo)
def create_todo(todo: schemas.ToDoCreate, db: Session = Depends(get_db)):
    db_todo = models.ToDo(title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos/", response_model=list[schemas.ToDo])
def read_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.ToDo).offset(skip).limit(limit).all()

@app.get("/todos/{todo_id}", response_model=schemas.ToDo)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=schemas.ToDo)
def update_todo(todo_id: int, todo: schemas.ToDoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="ToDo not found")

    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.completed = todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="ToDo not found")
    db.delete(db_todo)
    db.commit()
    return {"ok": True}
