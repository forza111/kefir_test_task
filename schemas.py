from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field, Extra


class UsersListElementModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True

class UpdateUserResponseModel(UsersListElementModel):
    other_name: str
    phone: str
    birthday: date

    class Config:
        orm_mode = True

class PrivateDetailUserResponseModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    other_name: str = None
    phone: str = None
    birthday: date = None
    city: int = None
    additional_info: str = None
    is_admin: bool = None

    class Config:
        orm_mode = True

class CurrentUserResponseModel(BaseModel):
    first_name: str
    last_name: str
    other_name: str
    email: str
    phone: str
    birthday: date
    is_admin: bool

    class Config:
        orm_mode = True

class PrivateCreateUserModel(BaseModel):
    login: str
    password: str
    first_name: str
    last_name: str
    email: str
    other_name: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None
    city: Optional[int] = None
    additional_info: Optional[str] = None
    is_admin: Optional[bool] = None

class UpdateUserModel(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    other_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None

    class Config:
        orm_mode = True

class PrivateUpdateUserModel(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    other_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None
    city: Optional[int] = None
    additional_info: Optional[str] = None
    is_admin: Optional[bool] = None

class PaginatedMetaDataModel(BaseModel):
    total: int
    page: int
    size: int

class CitiesHintModel(BaseModel):
    id: int
    name: str

class PrivateUsersListHintMetaModel(BaseModel):
    city: List[CitiesHintModel]

class UsersListMetaDataModel(BaseModel):
    pagination: PaginatedMetaDataModel

class PrivateUsersListMetaDataModel(UsersListMetaDataModel):
    hint: PrivateUsersListHintMetaModel

class UsersListResponseModel(BaseModel):
    data: List[UsersListElementModel]
    meta: UsersListMetaDataModel

class PrivateUsersListResponseModel(UsersListResponseModel):
    meta: PrivateUsersListMetaDataModel

class ErrorResponseModel(BaseModel):
    code: int
    message: str

class ValidationError(BaseModel):
    loc: List[str] = Field(title="Location")
    msg: str = Field(title="Message")
    type: str = Field(title="Error Type")

class HTTPValidationError(BaseModel):
    detail: List[ValidationError] = None

class HttpBaseError(BaseModel):
    title: str

class LoginModel(BaseModel):
    login: str
    password: str

    class Config:
        orm_mode = True