from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    role = Column(String, default='user')    # 'author' or 'user'


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(150), unique=True, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))

    authors = relationship('Author', back_populates='books')


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, autoincrement=True, primary_key=True)
    authorname = Column(String(50), unique=True)

    books = relationship('Book', back_populates='authors')
