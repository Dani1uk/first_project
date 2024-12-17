# from passlib.context import CryptContext
# from jose import jwt

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def get_password_hash(password: str) -> str:
#     return pwd_context.hash(password)


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)
def func(a, b=[]):
    b.apppend(a)
    return b 

func(1)
print(func(2, [10, 20]))
print(func(3))