from fastapi import Depends, APIRouter, HTTPException, Request, Form, Body, Header, Response
# from fastapi_session import Session as FastApiSession
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from .database import SessionLocal
from .models import User, Book, Author
from .schemas import UserCreate, BookCreate, UserLogin

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


@user_router.post('/register/')
async def register(
        # response: Response,
        user_data: UserCreate,
        db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    if user_data.role == 'author':
        new_author = Author(authorname=user_data.username)
        db.add(new_author)
        db.commit()
        db.refresh(new_author)

    new_user = User(username=user_data.username, password=user_data.password, role=user_data.role)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

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
    books = db.query(Book).join(Author).all()
    return templates.TemplateResponse("books.html", {"request": request, "books": books})


@book_router.post('/create_book/')
def create_book(
        book: BookCreate,
        db: Session = Depends(get_db),
):
    print(book.author_name)

    author = db.query(Author).filter(Author.authorname == book.author_name).first()
    print(author)
    if not author:
        raise HTTPException(
            status_code=404,
            detail=f"Author with id {book.author_id} not found"
        )

    existing_book = db.query(Book).filter(Book.title == book.title).first()
    if existing_book:
        raise HTTPException(status_code=400, detail="Book already exists")

    new_book = Book(title=book.title, author_id=author.id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return JSONResponse({
        "status": "success",
        "message": f"Book '{new_book.title}' created",
        "book": {
            "id": new_book.id,
            "title": new_book.title,
            "author_name": author.authorname
        }
    })


@book_router.delete('/delete_book/{book_id}')
def delete_book(
        book_id: int,
        author_name: str = Body(..., embed=True),
        db: Session = Depends(get_db)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    author = db.query(Author).filter(Author.authorname == author_name).first()
    if not author:
        raise HTTPException(status_code=404, detail=f"Author '{author_name}' not found")

    if book.author_id != author.id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own books"
        )

    db.delete(book)
    db.commit()

    return JSONResponse({
        "status": "success",
        "message": f"Book '{book.title}' deleted successfully",
        "book_id": book_id
    })


@book_router.put('/update_book/{book_id}')
def update_book(
        book_id: int,
        data: dict = Body(...),
        db: Session = Depends(get_db)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    author = db.query(Author).filter(Author.authorname == data['author_name']).first()
    if not author or book.author_id != author.id:
        raise HTTPException(
            status_code=403,
            detail="You can only update books you authored"
        )

    book.title = data['new_title']
    db.commit()
    db.refresh(book)

    return JSONResponse({
        "status": "success",
        "message": "Book updated",
        "book": {
            "id": book.id,
            "title": book.title,
            "author_name": author.authorname
        }
    })
