from sqlalchemy.orm import Session
import paginate_sqlalchemy

import models
from auth import Authenticate


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
    db.query(models.UserDetail).filter(models.UserDetail.id == id).update(update_user_body.dict(exclude_defaults=True),
                                                                          synchronize_session=False)
    db.commit()
    users = db.query(models.UserDetail).get(id)
    return users

def get_user(db: Session, pk):
    user = db.query(models.UserDetail).filter(models.UserDetail.id == pk).first()
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
