from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Date, BOOLEAN
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

from database import Base

class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    password = Column(String(60))

    class Config:
        orm_mode = True

class UserDetail(Base):
    __tablename__ = "user_detail"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(User.id), unique=True, nullable=False)
    user = relationship('User', backref=backref("user_detail", uselist=False))
    first_name = Column(String(40), nullable=False)
    last_name = Column(String(40), nullable=False)
    other_name = Column(String(40), nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String(12), nullable=False)
    birthday = Column(Date, nullable=False)
    is_admin = Column(BOOLEAN, default=False, nullable=False)
    city_id = Column(Integer, ForeignKey(City.id))
    city = relationship('City', backref=backref("user", uselist=False))




