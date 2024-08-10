from fastapi import FastAPI
from .database import base, engine
from app.movies import movies_router
from app.users import users_router

base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(movies_router.router)
app.include_router(users_router.router)
