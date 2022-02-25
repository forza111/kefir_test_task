from sqlalchemy.orm import Session
import paginate_sqlalchemy

import models
from auth import Authenticate
from fastapi import Response
from fastapi.responses import JSONResponse


required_not_empty_update_fields = ['first_name', 'last_name', 'email']

def check_required_fields_for_empty_values(update_body):
    body_keys = update_body.keys()
    req_fields_in_body = [i for i in required_not_empty_update_fields if i in body_keys]
    empty_fiels = [key for key in req_fields_in_body if not bool(update_body.get(key))]
    if empty_fiels:
        return JSONResponse(status_code=400, content={
            "code": 400,
            "message": f"field(s) {','.join(empty_fiels)} cannot have an empty value"})

def get_users(db: Session, page_n, size):
    users = db.query(models.UserDetail)
    page = paginate_sqlalchemy.SqlalchemyOrmPage(users, page=page_n, items_per_page=size,db_session=db)
    return {"data": page.items, "meta": {"pagination": {"total": page.page_count, "page": page_n, "size": size}}}

def get_private_users(db: Session, page_n, size):
    users = db.query(models.UserDetail)
    page = paginate_sqlalchemy.SqlalchemyOrmPage(users, page=page_n, items_per_page=size,db_session=db)
    return {"data": page.items, "meta": {"pagination": {"total": page.page_count, "page": page_n, "size": size},
                                         "hint": {"city": [{"id": 1, "name": "Moscow"}]}}}
# Уточнить, какие данные должны быть в "hint"

def update_db_user(db: Session, id, update_user_body):
    update_user_detail_body_dict = update_user_body.dict(exclude_unset=True)
    email = update_user_detail_body_dict.get("email")
    if email:
        if get_user_by_email(db, email):
            return JSONResponse(status_code=400, content={"code": 400,
                                                          "message": f"User with this email already exist"})
    empty_required_fiels = check_required_fields_for_empty_values(update_user_detail_body_dict)
    if empty_required_fiels:
        return empty_required_fiels

    if update_user_detail_body_dict:
        db.query(models.UserDetail).filter(models.UserDetail.id == id).update(
            update_user_body.dict(exclude_unset=True), synchronize_session=False)
        db.commit()
    user_detail = get_user_detail(db, id)
    return user_detail

def update_private_db_user(db: Session, id, update_user_body):
    update_user_detail_body_dict = update_user_body.dict(exclude_unset=True)
    new_id = update_user_detail_body_dict.pop("id")
    email = update_user_detail_body_dict.get("email")

    if id != new_id:
        exist_user = get_user(db, new_id)
        if exist_user:
            return JSONResponse(status_code=400, content={"code": 400,
                                                          "message": f"User with this id already exist"})
        db.query(models.User).filter(models.User.id == id).update({"id": new_id}, synchronize_session=False)
        db.commit()

    if email:
        if get_user_by_email(db, email):
            return JSONResponse(status_code=400, content={"code": 400,
                                                          "message": f"User with this email already exist"})

    empty_required_fiels = check_required_fields_for_empty_values(update_user_detail_body_dict)
    if empty_required_fiels:
        return empty_required_fiels

    if update_user_detail_body_dict:
        db.query(models.UserDetail).filter(models.UserDetail.id == new_id).update(update_user_detail_body_dict,
                                                                              synchronize_session=False)
        db.commit()

    user_detail = get_user_detail(db, new_id)
    return user_detail

def get_user_detail(db: Session, pk):
    user = db.query(models.UserDetail).filter(models.UserDetail.id == pk).first()
    return user

def get_user(db: Session, pk):
    user = db.query(models.User).filter(models.User.id == pk).first()
    return user

def get_user_by_email(db: Session, email):
    user = db.query(models.User).filter(models.UserDetail.email == email).first()
    return user

def create_db_user(db: Session, create_user_detail_body):
    create_user_detail_body_dict = create_user_detail_body.dict()
    create_user_body_dict = {"login": create_user_detail_body_dict.pop("login"),
                             "password": Authenticate.get_password_hash(create_user_detail_body_dict.pop("password"))}
    db_user = models.User(**create_user_body_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    create_user_detail_body_dict["id"] = db_user.id
    user = create_db_user_detail(db, create_user_detail_body_dict)
    return user

def create_db_user_detail(db: Session, user_body):
    db_user_detail = models.UserDetail(**user_body)
    db.add(db_user_detail)
    db.commit()
    db.refresh(db_user_detail)
    return db_user_detail

def get_city(db: Session, id):
    user = db.query(models.City).filter(models.City.id == id).first()
    return user

def delete_user(db: Session, delete_user):
    db.delete(delete_user)
    db.commit()
    db.close()
    return Response(status_code=204)

def create_city(db: Session, city):
    db_city = models.City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city