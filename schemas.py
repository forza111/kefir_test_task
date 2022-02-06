from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field, Extra


class UsersListElementModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

class UpdateUserResponseModel(UsersListElementModel):
    other_name: str
    phone: str
    birthday: date

class PrivateDetailUserResponseModel(UpdateUserResponseModel):
    city: int
    additional_info: str
    is_admin: bool

class CurrentUserResponseModel(BaseModel):
    first_name: str
    last_name: str
    other_name: str
    email: str
    phone: str
    birthday: date
    is_admin: bool

class PrivateCreateUserModel(CurrentUserResponseModel):
    other_name: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None
    city: Optional[int] = None
    additional_info: Optional[str] = None
    is_admin: Optional[bool] = None
    password: str

class UpdateUserModel(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    other_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None

class PrivateUpdateUserModel(UpdateUserModel):
    id: int
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

class LoginModel(BaseModel):
    login: str
    password: str
