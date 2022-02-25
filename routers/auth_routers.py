from fastapi import Request, APIRouter, Depends,Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from auth import Authenticate
from database import get_db
import schemas


router = APIRouter(tags=["auth"])

@router.post("/login",
             response_model=schemas.CurrentUserResponseModel,
             responses={400: {"model": schemas.ErrorResponseModel}}
             )
async def login(request: Request,body_user: schemas.LoginModel,response: Response, db: Session = Depends(get_db)):
    user = Authenticate.get_user_by_login(db,body_user.login)
    if user is None or not Authenticate.verify_password(body_user.password, user.password):
        return JSONResponse(status_code=400, content={"code": 400, "message": "Wrong login or password"})
    if Authenticate.verify_password(body_user.password, user.password):
        data = {"sub": body_user.login}
        token = Authenticate.create_access_token(data,request)
        response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
        return user.user_detail


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    response.status_code = 200
    return response