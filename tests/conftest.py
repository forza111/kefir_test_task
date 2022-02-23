from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import pytest

import database
import main
import models
import crud
import schemas


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    database.Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    db = Session(bind=connection)
    yield db
    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    main.app.dependency_overrides[database.get_db] = lambda: db
    with TestClient(main.app) as c:
        yield c


@pytest.fixture
def create_items(db):
    crud.create_city(db, schemas.CitiesHintModel(id=1, name="Moscow")),
    crud.create_db_user(db, schemas.PrivateCreateUserModel(
        login="admin",
        password="admin",
        first_name="Nikitos",
        last_name="Ionkin",
        email="nik@mail.com",
        other_name="Forza",
        phone="89119119119",
        birthday="1994-06-03",
        city=1,
        additional_info="I'm an engineer",
        is_admin=True)
    )