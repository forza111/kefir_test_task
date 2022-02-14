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


@app.post("/login",
          response_model=schemas.CurrentUserResponseModel,
          responses={400: {"model": schemas.ErrorResponseModel}})
async def login(request: Request,body_user: schemas.LoginModel,response: Response, db: Session = Depends(get_db)):
    user = Authenticate.get_user_by_login(db,body_user.login)
    if user is None or not Authenticate.verify_password(body_user.password, user.password):
        return JSONResponse(status_code=400, content={"code": 400, "message": "Wrong login or password"})
    if Authenticate.verify_password(body_user.password, user.password):
        data = {"sub": body_user.login}
        token = Authenticate.create_access_token(data,request)
        response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
        return user.user_detail

@app.get("/users/current",
         response_model=schemas.CurrentUserResponseModel,
         responses={400: {"model": schemas.ErrorResponseModel,
                          },
                    401: {"model": schemas.HttpBaseError,
                          "content": {
                              "application/json": {
                                  "example": {"title": "Response 401 Current User Users Current Get"}
                              }
                          }
                          }}
         )
async def get_current_user(
        current_user: schemas.LoginModel = Depends(Authenticate.get_current_user),
        db: Session = Depends(get_db)
        ):
    if current_user is None:
        return JSONResponse(status_code=401, content={"title": "Response 401 Current User Users Current Get"})
    return current_user.user_detail


@app.get("/users",
         response_model=schemas.UsersListResponseModel,
         responses={400: {"model": schemas.ErrorResponseModel,
                          },
                    401: {"model": schemas.HttpBaseError,
                          "content": {
                              "application/json": {
                                  "example": {"title": "Response 401 Users Users Get"}
                              }
                          }
                          }}
         )
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


@app.patch("/users/{pk}",
            response_model=schemas.UpdateUserResponseModel,
            responses = {
                400: {"model": schemas.ErrorResponseModel},
                401: {"model": schemas.HttpBaseError,
                      "content": {
                          "application/json": {"example": {"title": "Response 401 Edit User Users  Pk  Patch"}}
                      }
                      },
                404: {"model": schemas.HttpBaseError,
                      "content": {
                          "application/json": {"example": {"title": "Response 404 Edit User Users  Pk  Patch"}}
                      }
                      }
            }
           )
async def edit_user(
        pk: int,
        update_user_body: schemas.UpdateUserModel,
        current_user: schemas.LoginModel = Depends(Authenticate.get_current_user),
        db: Session = Depends(get_db)
        ):
    if current_user is None:
        return JSONResponse(status_code=401, content={"title": "Response 401 Current User Users Current Get"})
    request_user = crud.get_user(db, pk)
    if request_user is None:
        return JSONResponse(status_code=404, content={"title": "Response 404 Edit User Users  Pk  Patch"})
    if current_user.id != pk:
        return JSONResponse(status_code=400, content={"code": 400, "message": "The user can only change their information"})
    update_user = crud.update_db_user(db, pk, update_user_body)
    return update_user


@app.get("/private/users",
         response_model=schemas.PrivateUsersListResponseModel,
         responses={
             400: {"model": schemas.ErrorResponseModel},
             401: {"model": schemas.HttpBaseError,
                   "content": {
                       "application/json": {"example": {"title": "Response 401 Private Users Private Users Get"}}
                   }
                   },
             403: {"model": schemas.HttpBaseError,
                   "content": {
                       "application/json": {"example": {"title": "Response 403 Private Users Private Users Get"}}
                   }
                   }
         }
         )
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
          responses={
             400: {"model": schemas.ErrorResponseModel},
             401: {"model": schemas.HttpBaseError,
                   "content": {
                       "application/json": {"example": {"title": "Response 401 Private Create Users Private Users Post"}}
                   }
                   },
             403: {"model": schemas.HttpBaseError,
                   "content": {
                       "application/json": {"example": {"title": "Response 403 Private Create Users Private Users Post"}}
                   }
                   }
         }
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
         responses={400: {"model": schemas.ErrorResponseModel,
                          },
                    401: {"model": schemas.HttpBaseError,
                          "content": {
                              "application/json": {
                                  "example": {"title": "Response 401 Private Get User Private Users  Pk  Get"}
                              }
                          }
                          },
                    403: {"model": schemas.HttpBaseError,
                          "content": {
                              "application/json": {
                                  "example": {"title": "Response 403 Private Get User Private Users  Pk  Get"}
                              }
                          }
                          },
                    404: {"model": schemas.HttpBaseError,
                          "content": {
                              "application/json": {
                                  "example": {"title": "Response 404 Private Get User Private Users  Pk  Get"}
                              }
                          }
                          }
                     }
         )
async def get_users(
        pk: int,
        current_user: schemas.LoginModel = Depends(Authenticate.get_current_user),
        db: Session = Depends(get_db)
        ):
    if current_user is None:
        return JSONResponse(status_code=401, content={"title": "Response 401 Private Get User Private Users  Pk  Get"})
    if not current_user.user_detail.is_admin:
        return JSONResponse(status_code=403, content={"title": "Response 403 Private Get User Private Users  Pk  Get"})
    user = crud.get_user(db,pk)
    if user is None:
        return JSONResponse(status_code=404, content={"title": "Response 404 Private Get User Private Users  Pk  Get"})
    return user