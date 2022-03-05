from db.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends,Request
from jose import jwt
from passlib.context import CryptContext
from apps import crud

SECRET_KEY = "461554dcb6e1169277a0658acdb9b4634caf0c901fa63aaf5d3d9aa48f141056"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Dependencies:
    @staticmethod
    async def get_current_user(request: Request,db: Session = Depends(get_db)):
        '''Checks cookies for the presence of a token. in the absence of a token, returns to None. If a valid token
        is found, will return the authorized user.'''
        token = request.cookies.get("access_token")
        if token is None:
            return None
        scheme, _, param = token.partition(" ")
        payload = jwt.decode(param, SECRET_KEY, algorithms=ALGORITHM)
        id = payload.get("sub")
        user = crud.find_user(db,id)
        return user

    @staticmethod
    async def get_admin_user(request: Request,db: Session = Depends(get_db)):
        admin_user = Dependencies.get_current_user(request, db)
        if admin_user.is_admin:
            return admin_user
        else:
            return {"user": "not admin"}

    @staticmethod
    def create_access_token(data: dict, request: Request):
        '''Token creation. The function accepts data in the form of a dictionary'''
        jwt_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return jwt_token


    @staticmethod
    def get_password_hash(password):
        '''Hash password'''
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password, hashed_password):
        '''Check password and hash password version'''
        return pwd_context.verify(plain_password, hashed_password)