from pydantic import BaseModel


class UserSchema(BaseModel):
    uid: int
    uname: str
    email: str
    email_verified: bool
    role: str