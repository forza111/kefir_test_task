from datetime import datetime

from fastapi import Request, APIRouter, Depends, Form, HTTPException, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
# from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel

from auth import Authenticate
import crud
import models
from database import get_db
import schemas


app = APIRouter(tags=["notes"])


@app.post("/login", response_model=schemas.CurrentUserResponseModel, responses={
    400: {"model": schemas.ErrorResponseModel, "description": "Bad Request"},
})
async def login(request: Request,body_user: schemas.LoginModel,response: Response, db: Session = Depends(get_db)):
    user = Authenticate.get_user_by_login(db,body_user.login)
    if user is None or not Authenticate.verify_password(body_user.password, user.password):
        return JSONResponse(status_code=400, content={"code": 400, "message": "Wrong login or password"})
    if Authenticate.verify_password(body_user.password, user.password):
        data = {"sub": body_user.login}
        token = Authenticate.create_access_token(data,request)
        response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
        return user.user_detail

@app.get("/users/current", response_model=schemas.CurrentUserResponseModel)
async def get_current_user(
        current_user: schemas.LoginModel = Depends(Authenticate.get_current_user),
        db: Session = Depends(get_db)
        ):
    if current_user is None:
        return JSONResponse(status_code=401, content={"title": "Response 401 Current User Users Current Get"})
    return current_user.user_detail

@app.get("/users", response_model=schemas.UsersListResponseModel)
async def get_users(
        page: int, size: int,
        current_user: schemas.LoginModel = Depends(Authenticate.get_current_user),
        db: Session = Depends(get_db)
        ):
    if current_user is None:
        return JSONResponse(status_code=401, content={"title": "Response 401 Current User Users Current Get"})
    users = crud.get_users(db, page, size)
    return users

@app.patch("/users/{pk}", response_model=schemas.UpdateUserResponseModel, response_model_exclude_none=True)
async def update_user(
        update_user_body: schemas.UpdateUserModel,
        current_user: schemas.LoginModel = Depends(Authenticate.get_current_user),
        db: Session = Depends(get_db)
        ):
    if current_user is None:
        return JSONResponse(status_code=401, content={"title": "Response 401 Current User Users Current Get"})
    update_user = crud.update_db_user(db, current_user.id, update_user_body)
    return update_user