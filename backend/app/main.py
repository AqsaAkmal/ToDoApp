# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List
import models, schemas, crud, auth, database
from jose import JWTError, jws

models.Base.metadata.create_all(bind=database.engine)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

@app.post("/register/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/todos/", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return crud.create_todo(db=db, todo=todo, user_id=current_user.id)

@app.get("/todos/", response_model=List[schemas.Todo])
def read_todos(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return crud.get_todos(db=db, user_id=current_user.id, skip=skip, limit=limit)

@app.delete("/todos/{todo_id}", response_model=List[schemas.Todo])
def delete_todo(todo_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    db_todo = crud.delete_todo(db=db,todo_id=todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail=f"Todo item with id {todo_id} not found")
    return crud.get_todos(db=db, user_id=current_user.id, skip=0, limit=10)  # Return updated list after deletion
