from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from fastapi import Depends,Request,Response
from fastapi.templating import Jinja2Templates
from jose import jwt

import dependencies
import models
import database

# templates = Jinja2Templates(directory="templates")


class Authenticate:
    @staticmethod
    def authenticate_user(db: Session, login: str, password: str):
        '''
        The function takes 2 arguments - login and password. The first step is to search the database by email,
        if there is no user with such email, the function returns False. If a user with such an email exists, the
        password is checked (entered in the form and in the database, which is hashed).
        If the password is incorrect, it returns False, if everything went well, then it returns the user
        '''
        user = Authenticate.get_user_by_login(db, login)
        if not user:
            return False
        if not Authenticate.verify_password(password, user.password):
            return False
        return user

    @staticmethod
    async def get_current_user(request: Request,db: Session = Depends(database.get_db)):
        '''Checks cookies for the presence of a token. in the absence of a token, returns to None. If a valid token
        is found, will return the authorized user.'''
        token = request.cookies.get("access_token")
        if token is None:
            return None
        scheme, _, param = token.partition(" ")
        payload = jwt.decode(param, dependencies.SECRET_KEY, algorithms=dependencies.ALGORITHM)
        login = payload.get("sub")
        user = Authenticate.get_user_by_login(db,login)
        return user

    @staticmethod
    async def get_admin_user(request: Request,db: Session = Depends(database.get_db)):
        current_user = Authenticate.get_current_user(request, db)
        if current_user.user_detail.is_admin:
            return current_user
        else: return {"user": "not admin"}


    @staticmethod
    def create_access_token(data: dict, request: Request):
        '''Token creation. The function accepts data in the form of a dictionary'''
        jwt_token = jwt.encode(data, dependencies.SECRET_KEY, algorithm=dependencies.ALGORITHM)
        return jwt_token
        # response = Response()
        # response.set_cookie(key="access_token", value=f"Bearer {jwt_token}", httponly=True)
        # return {"first_name":"1", "last_name":"2", "other_name":'23', "email":'1', "phone":"123123", "birthday": '1994-03-02', "is_admin": True}

    @staticmethod
    def get_user(db: Session, user_id: int):
        '''Get user by id'''
        return db.query(models.User).filter(models.User.id == user_id).first()

    @staticmethod
    def get_user_by_login(db: Session, login: str):
        '''Get user by login'''
        return db.query(models.User).filter(models.User.login == login).first()

    @staticmethod
    def get_password_hash(password):
        '''Hash password'''
        return dependencies.pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password, hashed_password):
        '''Check password and hash password version'''
        return dependencies.pwd_context.verify(plain_password, hashed_password)