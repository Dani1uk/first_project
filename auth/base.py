from auth.orm import AsyncORM
from models import User


class UserBase(AsyncORM):
    model = User
