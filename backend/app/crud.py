# backend/app/crud.py
from sqlalchemy.orm import Session
import models, schemas, auth

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_todos(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Todo).filter(models.Todo.owner_id == user_id).offset(skip).limit(limit).all()

def get_todo_by_id(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()

def create_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = models.Todo(**todo.dict(), owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int):
    db_todo = get_todo_by_id(db, todo_id)
    db.delete(db_todo)
    db.commit()
    return db_todo
