from typing import Annotated

from pydantic import BaseModel
from sqlalchemy.orm import Session
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Path
import models
from models import Todos
from database import engine, SessionLocal
from starlette import status


if __name__ == '__main__':
  uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) 


app = FastAPI()

models.Base.metadata.create_all(bind = engine)


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
  return db.query(Todos).all()


@app.get("/todos/{todo_id}", status_code=status.HTTP_200_OK )
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
  todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
  if todo_model is not None:
    return todo_model
  raise HTTPException(status_code=404, detail="Todo not found.")
