from pydantic import BaseModel, field_validator


class PasswordSignInRequest(BaseModel):
    id: str
    password: str
    recaptcha: str

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
