from typing import Annotated

from pydantic import BaseModel
from sqlalchemy.orm import Session
import uvicorn # importing the server
from fastapi import FastAPI, Depends, HTTPException, Path
import models
from models import Todos
from database import engine, SessionLocal
from starlette import status


if __name__ == '__main__':
  uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) 


app = FastAPI()

models.Base.metadata.create_all(bind = engine)
# The above line will only be ran if our todos.db doesn't exist.
# So if we go back to models.py and enhance todos table, this will not run automatically and enhance the tabes.
# with this quick and east way of creating databases, it's easier just to delete todos.db and then recreate it if we add anything extra to our todos.
# Alembic Section will tech how to enhance DB without deleting each time.

# now we know there are only three records inside. so we create our DB dependency:
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
# The 'yield' means only the code prior to and including yield statement is executed before sending a response.
# The code following the yield statement is executed after the response has been delivered. 
# This makes fastApi quickerm because we can fetch information from a database, return it to the client and then close off the connection to the database after. 

# before each request, we need to be able to fetch this db sessionlocal and open up and then close a connection on every request sent to this fastapi application.
# Here we create the dependency; we say this function relies on our db opening up (get_db()),
# We want to create a session and being able to then return that information back to us and close the session.
# in this function we say we want to return all of our todos (which we need to import from our models)
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
