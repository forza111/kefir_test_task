from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class CitiesHintModel(BaseModel):
    id: int
    name: str

class LoginModel(BaseModel):
    login: str
    password: str

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
    birthday: Optional[str] = None
    city: Optional[int] = None
    additional_info: Optional[str] = None
    password: str


class ErrorResponseModel(BaseModel):
    code: int
    message: str

class ValidationError(BaseModel):
    loc: List[str] = Field(title="Location")
    msg: str = Field(title="Message")
    type: str = Field(title="Error Type")

class HTTPValidationError(BaseModel):
    detail: List[ValidationError] = None

class PaginatedMetaDataModel(BaseModel):
    total: int
    page: int
    size: int



