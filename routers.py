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


@app.post("/login", response_model=schemas.CurrentUserResponseModel, responses={
    400: {"model": schemas.ErrorResponseModel, "description": "Bad Request"},
})
async def login(body_user: schemas.LoginModel,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.login == body_user.login).first()
    if user is None or not Authenticate.verify_password(body_user.password, user.password):
        return JSONResponse(status_code=400, content={"code": 400, "message": "Wrong login or password"})
    if Authenticate.verify_password(body_user.password, user.password):
        user_detail = user.user_detail
        return {"first_name": user_detail.first_name, "last_name": user_detail.last_name,
                "other_name": user_detail.other_name, "email": user_detail.email,
                "phone": user_detail.phone, "birthday": user_detail.birthday,
                "is_admin": user_detail.is_admin
                }
