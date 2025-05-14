from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    role: str = 'user'


class UserLogin(BaseModel):
    username: str
    password: str


class BookCreate(BaseModel):
    title: str
    author_name: str
