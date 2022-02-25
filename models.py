from sqlalchemy import Column, ForeignKey, Integer, String, Date, BOOLEAN
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

from database import Base

class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

    class Config:
        orm_mode = True

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    login = Column(String, unique=True, index=True)
    password = Column(String(60))

    class Config:
        orm_mode = True

class UserDetail(Base):
    __tablename__ = "user_detail"
    id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, index=True)
    user = relationship('User', backref=backref("user_detail", uselist=False, passive_deletes=True))
    first_name = Column(String(40), nullable=False)
    last_name = Column(String(40), nullable=False)
    other_name = Column(String(40), nullable=True)
    email = Column(String(50), unique=True, nullable=False)
    phone = Column(String(12), nullable=True)
    birthday = Column(Date, nullable=True)
    is_admin = Column(BOOLEAN, default=False, nullable=True)
    city = Column(Integer, ForeignKey(City.id), nullable=True)
    city_detail = relationship('City', backref=backref("user", uselist=False))
    additional_info = Column(String(100), nullable=True)




