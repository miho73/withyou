import re
from typing import Optional

from pydantic import BaseModel, field_validator

from models.user import Role


class UserSchema(BaseModel):
    uid: Optional[int] = None
    uname: str
    email: str
    email_verified: bool
    role: Role = Role.USER
    sex: str = 'N'

    @field_validator("email", mode="before")
    @classmethod
    def validate(cls, value):
        if len(value) < 5 or len(value) > 255:
            raise ValueError("Email must be 5 to 255 characters long")
        if not re.match(r'^[-\w.]+@([-\w]+.)+[-\w]{2,4}$', value):
            raise ValueError("Email regex check failed")
        return value

    @field_validator("uname", mode="before")
    @classmethod
    def validate_name(cls, value):
        if len(value) < 1 or len(value) > 100:
            raise ValueError("Name must be 1 to 100 characters long")
        return value

    @field_validator("role", mode="before")
    @classmethod
    def validate_role(cls, value):
        if value.value not in ["USER", "ADMIN"]:
            raise ValueError("Role must be one of 'USER' or 'ADMIN'")
        return value

    @field_validator("sex", mode="before")
    @classmethod
    def validate_sex(cls, value):
        if value not in ["M", "F", "N"]:
            raise ValueError("Sex must be one of M, F, N")
        return value


class GoogleUser(UserSchema):
    id: str
    picture: str


class KakaoUser(UserSchema):
    id: str
    picture: str
    birthday: str
    gender: str

class JwtUser(BaseModel):
    uid: int
    uname: str
    email: str
    email_verified: bool
    role: Role

    @field_validator("email", mode="before")
    @classmethod
    def validate(cls, value):
        if len(value) < 5 or len(value) > 255:
            raise ValueError("Email must be 5 to 255 characters long")
        if not re.match(r'^[-\w.]+@([-\w]+.)+[-\w]{2,4}$', value):
            raise ValueError("Email regex check failed")
        return value

    @field_validator("uname", mode="before")
    @classmethod
    def validate_name(cls, value):
        if len(value) < 1 or len(value) > 100:
            raise ValueError("Name must be 1 to 100 characters long")
        return value

    @field_validator("role", mode="before")
    @classmethod
    def validate_role(cls, value):
        if value.value not in ["USER", "ADMIN"]:
            raise ValueError("Role must be one of 'USER' or 'ADMIN'")
        return value
