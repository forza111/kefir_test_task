import re

from sqlalchemy.orm import Session
import paginate_sqlalchemy
from fastapi import Response
from fastapi.responses import JSONResponse

from apps import models
from api.depends import Dependencies


required_not_empty_update_fields = ['id','first_name', 'last_name', 'email', 'phone']


def get_user_by_email(db: Session, email: str):
    '''Get user by email'''
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_phone(db: Session, phone: str):
    '''Get user by phone'''
    return db.query(models.User).filter(models.User.phone == phone).first()

def find_user(db: Session, login: str):
    '''
    Find user.
    First, the search is checked by email, if not found, it is checked by phone number
    '''
    user = get_user_by_email(db, login)
    if user:
        return user
    user = get_user_by_phone(db, login)
    return user

def get_user_by_id(db: Session, user_id: int):
    '''Get user by id'''
    return db.query(models.User).filter(models.User.id == user_id).first()

def FieldIsEmail(email):
    regex = re.compile(
        r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\."
        r"[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
    if re.fullmatch(regex, email):
        return True

def FieldIsPhone(phone):
    regex = re.compile(r"\d{11}")
    if re.fullmatch(regex, phone):
        return True

def check_required_fields_for_empty_values(update_body):
    body_keys = update_body.keys()
    req_fields_in_body = [i for i in required_not_empty_update_fields if i in body_keys]
    empty_fiels = [key for key in req_fields_in_body if not bool(update_body.get(key))]
    if empty_fiels:
        return JSONResponse(status_code=400, content={
            "code": 400,
            "message": f"field(s) {','.join(empty_fiels)} cannot have an empty value"})

def check_used_fiels(db: Session, fields_to_check: dict):
    fields = fields_to_check.keys()
    if "id" in fields:
        user = get_user_by_id(db, fields_to_check["id"])
        if user:
            return JSONResponse(status_code=400, content={
                "code": 400,
                "message": f"user with this id already exists"})
    if "email" in fields:
        user = get_user_by_email(db, fields_to_check["email"])
        if user:
            return JSONResponse(status_code=400, content={
                "code": 400,
                "message": f"user with this email already exists"})
    if "phone" in fields:
        user = get_user_by_phone(db, fields_to_check["phone"])
        if user:
            return JSONResponse(status_code=400, content={
                "code": 400,
                "message": f"user with this phone already exists"})


def get_users(db: Session, page_n, size):
    users = db.query(models.User)
    page = paginate_sqlalchemy.SqlalchemyOrmPage(users, page=page_n, items_per_page=size,db_session=db)
    return {"data": page.items, "meta": {"pagination": {"total": page.page_count, "page": page_n, "size": size}}}

def get_private_users(db: Session, page_n, size):
    users = db.query(models.User)
    page = paginate_sqlalchemy.SqlalchemyOrmPage(users, page=page_n, items_per_page=size,db_session=db)
    return {"data": page.items, "meta": {"pagination": {"total": page.page_count, "page": page_n, "size": size},
                                         "hint": {"city": [{"id": 1, "name": "Moscow"}]}}}
# Уточнить, какие данные должны быть в "hint"

def update_db_user(db: Session, id, update_user_body, request, response):
    update_user_body_dict = update_user_body.dict(exclude_unset=True)
    empty_required_fiels = check_required_fields_for_empty_values(update_user_body_dict)
    if empty_required_fiels:
        return empty_required_fiels
    if update_user_body_dict:
        field_is_busy = check_used_fiels(db, update_user_body_dict)
        if field_is_busy:
            return field_is_busy
        db.query(models.User).filter(models.User.id == id).update(update_user_body_dict, synchronize_session=False)
        db.commit()
    user = get_user_by_id(db, id)
    new_email = update_user_body_dict.get("email")
    if new_email:
        data = {"sub": new_email}
        token = Dependencies.create_access_token(data,request)
        response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
    return user

def update_private_db_user(db: Session, id, current_user_id, update_user_body, request, response):
    update_private_user_body_dict = update_user_body.dict(exclude_unset=True)
    new_id = update_private_user_body_dict.get("id")
    empty_required_fiels = check_required_fields_for_empty_values(update_private_user_body_dict)
    if empty_required_fiels:
        return empty_required_fiels
    if update_private_user_body_dict:
        field_is_busy = check_used_fiels(db, update_private_user_body_dict)
        if field_is_busy:
            return field_is_busy
        db.query(models.User).filter(models.User.id == id).update(update_private_user_body_dict, synchronize_session=False)
        db.commit()
    if new_id:
        id = new_id
    user = get_user_by_id(db, id)
    new_email = update_private_user_body_dict.get("email")
    if id == current_user_id and new_email:
        data = {"sub": new_email}
        token = Dependencies.create_access_token(data, request)
        response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
    return user

def get_user_by_email(db: Session, email):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user

def create_db_user(db: Session, create_user_body):
    db_user = models.User(**create_user_body.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

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