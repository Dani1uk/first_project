from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
import re

    
class EmailModel(BaseModel):
    email: EmailStr = Field(description="Электронная почта")
    model_config = ConfigDict(from_attributes=True)

class UserBase(EmailModel):
    phone_number: str = Field(description="Номер телефона в международном формате, начинающийся с '+'")
    name: str = Field(min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    surname: str = Field(min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")

    @field_validator("phone_number")
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r'^\+\d{5,15}$', value):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 5 до 15 цифр')
        return value

class SUserRegister(UserBase):
    password: str = Field(min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")

class SUserAddDB(UserBase):
    password: str = Field(min_length=5, description="Пароль в формате HASH-строки")

# class SUserAuth(EmailModel):
#     password: str = Field(min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    
class SUserAuth(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
 
 