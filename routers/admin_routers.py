from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from auth import Authenticate
import crud
from database import get_db
import responses
import schemas


router = APIRouter(prefix='/private', tags=["admin"])


@router.get("/users", response_model=schemas.PrivateUsersListResponseModel, responses=responses.get_private_users)
async def private_users(
        page: int,
        size: int,
        current_user: schemas.LoginModel = Depends(Authenticate.get_current_user),
        db: Session = Depends(get_db)
        ):
    if current_user is None:
        return JSONResponse(status_code=401, content={"title": "Response 401 Private Users Private Users Get"})
    if not current_user.user_detail.is_admin:
        return JSONResponse(status_code=403, content={"title": "Response 403 Private Users Private Users Get"})
    users = crud.get_private_users(db, page, size)
    return users


@router.post("/users",
          response_model=schemas.PrivateDetailUserResponseModel,
          responses=responses.post_private_users
          )
async def private_create_users(
        create_user_body: schemas.PrivateCreateUserModel,
        current_user: schemas.LoginModel = Depends(Authenticate.get_current_user),
        db: Session = Depends(get_db)
        ):
    if current_user is None:
        return JSONResponse(status_code=401, content={"title": "Response 401 Private Create Users Private Users Post"})
    if not current_user.user_detail.is_admin:
        return JSONResponse(status_code=403, content={"title": "Response 403 Private Create Users Private Users Post"})
    if Authenticate.get_user_by_login(db,create_user_body.login):
        return JSONResponse(status_code=400, content={"code":400,
                                                      "message": "User with this login already exists"})
    if Authenticate.get_user_detail_by_email(db,create_user_body.email):
        return JSONResponse(status_code=400, content={"code":400,
                                                      "message": "User with this email already exists"})
    if crud.get_city(db,create_user_body.city) is None:
        return JSONResponse(status_code=400, content={"code":400,
                                                      "message": f"City {create_user_body.city} does not exist"})
    create_user = crud.create_db_user(db, create_user_body)
    return create_user


@router.get("/users/{pk}",
         response_model=schemas.PrivateDetailUserResponseModel,
         responses=responses.get_private_users_pk
         )
async def get_users(
        pk: int,
        current_user: schemas.LoginModel = Depends(Authenticate.get_current_user),
        db: Session = Depends(get_db)
        ):
    if current_user is None:
        return JSONResponse(status_code=401, content={"title": "Response 401 Private Get User Private Users Pk Get"})
    if not current_user.user_detail.is_admin:
        return JSONResponse(status_code=403, content={"title": "Response 403 Private Get User Private Users Pk Get"})
    user = crud.get_user_detail(db,pk)
    if user is None:
        return JSONResponse(status_code=404, content={"title": "Response 404 Private Get User Private Users Pk Get"})
    return user


@router.delete("/users/{pk}", status_code=204, responses=responses.delete_private_users_pk)
async def private_delete_user(
        pk: int,
        current_user: schemas.LoginModel = Depends(Authenticate.get_current_user),
        db: Session = Depends(get_db)
        ):
    if current_user is None:
        return JSONResponse(status_code=401,
                            content={"title": "Response 401 Private Delete User Private Users Pk Delete"})
    if not current_user.user_detail.is_admin:
        return JSONResponse(status_code=403,
                            content={"title": "Response 403 Private Delete User Private Users Pk Delete"})
    delete_user = crud.get_user(db,pk)
    if delete_user is None:
        return JSONResponse(status_code=404,
                            content={"title": "Response 404 Private Delete User Private Users Pk Delete"})
    return crud.delete_user(db, delete_user)


@router.patch("/users/{pk}",
           response_model=schemas.PrivateDetailUserResponseModel,
           responses=responses.patch_private_users_pk)
async def private_patch_user(
        pk: int,
        update_user_body: schemas.PrivateUpdateUserModel,
        current_user: schemas.LoginModel = Depends(Authenticate.get_current_user),
        db: Session = Depends(get_db)
        ):
    if current_user is None:
        return JSONResponse(status_code=401,
                            content={"title": "Response 401 Private Patch User Private Users Pk Patch"})
    if not current_user.user_detail.is_admin:
        return JSONResponse(status_code=403,
                            content={"title": "Response 403 Private Patch User Private Users Pk Patch"})
    request_user = crud.get_user_detail(db, pk)
    if request_user is None:
        return JSONResponse(status_code=404, content={"title": "Response 404 Edit User Users Pk Patch"})
    update_user = crud.update_private_db_user(db, pk, update_user_body)
    return update_user