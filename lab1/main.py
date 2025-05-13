from http.client import HTTPException

from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text, inspect
from sqlalchemy.orm import Session
import uvicorn

from src.database import SessionLocal, Base, engine
from src.endpoints import user_router, book_router, get_db
from src.models import User, Book

app = FastAPI(debug=True)
templates = Jinja2Templates(directory="templates")


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



app.include_router(user_router)
app.include_router(book_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
