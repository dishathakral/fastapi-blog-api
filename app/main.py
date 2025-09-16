from fastapi import FastAPI,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel 
from . import models,database_models,utils
from .database import engine,get_db
from typing import List
from sqlalchemy.orm import Session
from app. routers import posts,user,auth


app = FastAPI()
database_models.Base.metadata.create_all(bind=engine)
# try:
#     conn=psycopg2.connect(host='localhost',database='postgres',password='anku9729',user='postgres',cursor_factory=RealDictCursor)
#     print("database is succesfully connected!!")
#     cursor=conn.cursor()
# except Exception as error:
#     print("connection to databse is failed")
#     print(f"error:{error}") 
  

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# my_posts = [{"title": "title of post 1",
# "content": "content of post 1",'id':1},{"title": "favorite foods",
# "content": "I like pizza", "id": 2}] 

app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)
@app.get("/")
def read_root():
    return {"Hello": "World"}



