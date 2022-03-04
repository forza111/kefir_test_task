from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from auth import Authenticate
import crud
from database import get_db
import responses
import schemas


router = APIRouter(tags=["user"])


@router.get("/users/current", response_model=schemas.CurrentUserResponseModel, responses=responses.get_users_current)
async def get_current_user(
        current_user: schemas.LoginModel = Depends(Authenticate.get_current_user)
        ):
    if current_user is None:
        return JSONResponse(status_code=401, content={"title": "Response 401 Current User Users Current Get"})
    return current_user.user_detail


@router.get("/users", response_model=schemas.UsersListResponseModel, responses=responses.get_users)
async def get_users(
        page: int,
        size: int,
        current_user: schemas.LoginModel = Depends(Authenticate.get_current_user),
        db: Session = Depends(get_db)
        ):
    if current_user is None:
        return JSONResponse(status_code=401, content={"title": "Response 401 Current User Users Current Get"})
    users = crud.get_users(db, page, size)
    return users


@router.patch("/users/{pk}", response_model=schemas.UpdateUserResponseModel, responses=responses.patch_users_pk)
async def edit_user(
        update_user_body: schemas.UpdateUserModel,
        current_user: schemas.LoginModel = Depends(Authenticate.get_current_user),
        db: Session = Depends(get_db)
        ):
    if current_user is None:
        return JSONResponse(status_code=401, content={"title": "Response 401 Current User Users Current Get"})
    pk = current_user.id
    update_user = crud.update_db_user(db, pk, update_user_body)
    return update_user