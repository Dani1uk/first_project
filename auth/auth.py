
from datetime import datetime, timedelta, timezone
from pydantic import EmailStr
from base import UserBase
from config import get_auth_data
from utils import verify_password

def create_access_token(data: dict) -> str:
    """Служебная функция для генерации нового токена"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt

async def authenticate_user(email: EmailStr, password: str,):
    user = await UserBase.find_one_or_none(email=email)
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user