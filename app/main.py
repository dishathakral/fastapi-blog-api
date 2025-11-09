from fastapi import FastAPI
from fastapi.params import Body
from .config import Settings
from . import database_models
from .database import engine
from app. routers import posts,user,auth,votes
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    alLow_methods= ["*"],
    allow_headers=["*"],)
# database_models.Base.metadata.create_all(bind=engine)
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
app.include_router(votes.router)
@app.get("/")
def read_root():
    return {"Hello": "World"}



