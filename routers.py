from datetime import datetime

from fastapi import Request, APIRouter, Depends, Form, HTTPException, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
# from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel

from auth import Authenticate
import models
from database import get_db
import schemas


app = APIRouter(tags=["notes"])


@app.post("/login", response_model=schemas.LoginModel, responses={
    400: {"model": schemas.ErrorResponseModel, "description": "Bad Request"},
})
async def login(body_user: schemas.LoginModel,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.login == body_user.login).first()
    if user is None or not Authenticate.verify_password(body_user.password, user.password):
        return JSONResponse(status_code=400, content={"code": 400, "message": "Wrong login or password"})
    if Authenticate.verify_password(body_user.password, user.password):
        return {"login": user.login, "password": user.password}