from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import amount, user, baby, auth
from . import models
from .database import SessionLocal, engine

# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["http://localhost", "http://localhost:8080", "https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(amount.router)
app.include_router(user.router)
app.include_router(baby.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "app is up!"}
