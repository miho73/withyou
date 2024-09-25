import re

from pydantic import field_validator, BaseModel
from pydantic.v1 import Field


class AddUserRequest(BaseModel):
    name: str
    email: str
    sex: str = 'N'
    id: str
    password: str = Field(ge=6)
    recaptcha: str

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value):
        if len(value) < 1 or len(value) > 100:
            raise ValueError("Name must be 1 to 100 characters long")
        return value

    @field_validator("email", mode="before")
    @classmethod
    def validate(cls, value):
        if len(value) < 5 or len(value) > 255:
            raise ValueError("Email must be 5 to 255 characters long")
        if not re.match(r'^[-\w.]+@([-\w]+.)+[-\w]{2,4}$', value):
            raise ValueError("Email regex check failed")
        return value

    @field_validator("sex", mode="before")
    @classmethod
    def validate_sex(cls, value):
        if value not in ["M", "F", "N"]:
            raise ValueError("Sex must be one of M, F, N")
        return value

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, value):
        if len(value) < 1 or len(value) > 255:
            raise ValueError("Id must be under 255 characters long")
        return value

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 6:
            raise ValueError("Password must be over 6 characters long")
        return value

    @field_validator("recaptcha", mode="before")
    @classmethod
    def validate_recaptcha(cls, value):
        if value is None:
            raise ValueError("reCAPTCHA token was not passed")
        return value
