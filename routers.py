from fastapi import Request, APIRouter, Depends,Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from auth import Authenticate
import crud
from database import get_db
import responses
import schemas


app = APIRouter(tags=["notes"])


@app.post("/login",
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


@app.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    response.status_code = 200
    return response


@app.get("/users/current", response_model=schemas.CurrentUserResponseModel, responses=responses.get_users_current)
async def get_current_user(
        current_user: schemas.LoginModel = Depends(Authenticate.get_current_user),
        db: Session = Depends(get_db)
        ):
    if current_user is None:
        return JSONResponse(status_code=401, content={"title": "Response 401 Current User Users Current Get"})
    return current_user.user_detail


@app.get("/users", response_model=schemas.UsersListResponseModel, responses=responses.get_users)
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


@app.patch("/users/{pk}", response_model=schemas.UpdateUserResponseModel, responses=responses.patch_users_pk)
async def edit_user(
        pk: int,
        update_user_body: schemas.UpdateUserModel,
        current_user: schemas.LoginModel = Depends(Authenticate.get_current_user),
        db: Session = Depends(get_db)
        ):
    if current_user is None:
        return JSONResponse(status_code=401, content={"title": "Response 401 Current User Users Current Get"})
    request_user = crud.get_user_detail(db, pk)
    if request_user is None:
        return JSONResponse(status_code=404, content={"title": "Response 404 Edit User Users  Pk  Patch"})
    if current_user.id != pk:
        return JSONResponse(status_code=400, content={"code": 400,
                                                      "message": "The user can only change their information"})
    update_user = crud.update_db_user(db, pk, update_user_body)
    return update_user


@app.get("/private/users", response_model=schemas.PrivateUsersListResponseModel, responses=responses.get_private_users)
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


@app.post("/private/users",
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


@app.get("/private/users/{pk}",
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


@app.delete("/private/users/{pk}", status_code=204, responses=responses.delete_private_users_pk)
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


@app.patch("/private/users/{pk}",
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