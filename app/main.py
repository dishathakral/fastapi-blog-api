from fastapi import FastAPI
from fastapi.params import Body
from .config import Settings
from . import database_models
from .database import engine
from app. routers import posts,user,auth,votes
from fastapi.middleware.cors import CORSMiddleware
import os
app = FastAPI()
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods= ["*"],
    allow_headers=["*"],)

# Don't initialize database on startup if it fails
# Instead, handle it per-request
# try:
#     from .config import settings
#     from . import database_models
#     from .database import engine
#     from .routers import posts, user, auth, votes

#     # Only create tables if we can connect
#     try:
#         database_models.Base.metadata.create_all(bind=engine)
#     except Exception as db_error:
#         print(f"Database init warning: {db_error}")

app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

# except Exception as e:
#     print(f"Failed to load routers: {e}")
#     import traceback

#     traceback.print_exc()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/health")
def health_check():
    return {"status": "ok"}