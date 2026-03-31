from fastapi import FastAPI
from app.api.dogs import router as dogs_router

from app.db.session import engine
from app.db.base import Base

from app.models.dog import Dog


app = FastAPI(title="DOGS CRUD API")

@app.get("/")
def root():
    return {"hello": "world"}

@app.get("/health")
def health():
    return {"status": "ok"}

#Base.metadata.create_all(bind=engine)

app.include_router(dogs_router)