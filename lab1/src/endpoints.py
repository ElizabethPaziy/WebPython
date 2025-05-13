from fastapi import Depends, APIRouter, HTTPException, Request, Form, Body
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from .database import SessionLocal
from .models import User, Book
from .schemas import UserCreate, BookCreate

user_router = APIRouter(tags=['Users'], prefix='/users')
book_router = APIRouter(tags=['Books'], prefix='/books')

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- USERS ---


@user_router.get('/')
def get_all_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@user_router.post('/create_user/')
def create_user(
        user_data: UserCreate,
        db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(username=user_data.username, role=user_data.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # return {"message": f"User '{new_user.username}' was created successfully"}
    return {
        "status": "success",
        "message": f"User '{new_user.username}' was created successfully",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "role": new_user.role
        }
    }


# --- BOOKS ---
@book_router.get('/')
def get_all_books(request: Request, db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return templates.TemplateResponse("books.html", {"request": request, "books": books})


@book_router.post('/create_book/')
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    existing_book = db.query(Book).filter(Book.title == book.title).first()
    if existing_book:
        raise HTTPException(status_code=400, detail="Book already exists")
    new_book = Book(title=book.title, author_id=book.author_id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {
        "status": "success",
        "message": f"Book with title: '{new_book.title}' was created successfully",
        "book": {
            "id": new_book.id,
            "title": new_book.title,
            "author_id": new_book.author_id
        }
    }


@book_router.delete('/delete_book/{book_id}')
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book_title = book.title
    db.delete(book)
    db.commit()
    return {
        'status': 200,
        "message": f"Book with title: {book_title} was deleted successfully",
        "book_id": book_id
    }


@book_router.put('/update_book/{book_id}')
def update_book(book_id: int, new_book: BookCreate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = new_book.title
    book.author_id = new_book.author_id
    db.commit()
    db.refresh(book)
    return {
        "status": 200,
        "message": "Book was updated successfully",
        "book": {
            "id": book.id,
            "title": book.title,
            "author_id": book.author_id
        }
    }