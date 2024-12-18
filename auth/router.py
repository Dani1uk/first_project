from fastapi import APIRouter, HTTPException, Response, status
from auth.auth import authenticate_user, create_access_token
from auth.utils import get_password_hash
from auth.base import UserBase
from models import User
from auth.orm import AsyncORM
from auth.schemas import EmailModel, SUserAddDB, SUserAuth, SUserRegister
from fastapi import Depends
from database import Base, get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post("/register/")
async def register_user(user_data: SUserRegister, session: AsyncSession = Depends(get_db)) -> dict:
    user = await UserBase.find_one_or_none(session=session, filters=EmailModel(email=user_data.email))
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_dict = user_data.model_dump()
    user_dict['password'] = get_password_hash(user_data.password)
    await UserBase.add(session=session, values=SUserAddDB(**user_dict))
    return {'message': 'Вы успешно зарегистрированы!'}

@router.post("/login/")
async def auth_user(response: Response, user_data: SUserAuth, session: AsyncSession = Depends(get_db)):
    check = await authenticate_user(session=session ,email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token = create_access_token({"sub": str(check.user_id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}