from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import List, Optional

class User(BaseModel):
    username: str
    surname: str  
    user_id: int
    email: EmailStr = Field(default=None, description="Email пользователя")


class News(BaseModel):
    news_id: int
    date: date
    title: str
    link: str

class FavoriteNews(BaseModel):
    favorite_id: int
    news_id: int
    user_id: int


class UserLogin(BaseModel):
    login: str = Field(default=None, description="Email пользователя")
    hash_password: str = Field(default=None, description="Пароль пользователя")