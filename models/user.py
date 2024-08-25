from enum import Enum

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP, INTEGER, VARCHAR, BOOLEAN, CHAR
from sqlalchemy.orm import relationship

from sql.database import Base


class Role(Enum):
    ROLE_USER = "USER"
    ROLE_ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "users"}

    uid = Column(INTEGER, primary_key=True, index=True, unique=True, nullable=False, autoincrement=True)
    uname = Column(VARCHAR, nullable=False)

    join_date = Column(TIMESTAMP, nullable=False, default="now()")
    last_login = Column(TIMESTAMP)

    email = Column(VARCHAR, nullable=False, unique=True)
    email_verified = Column(BOOLEAN, nullable=False, default=False)
    role:Role = Column(CHAR, nullable=False, default="USER")

    auth_methods = relationship("AuthMethods", back_populates="user", uselist=False)

class GoogleUser:
    id: str
    email_verified: bool
    email: str

    uname: str
    picture: str

class KakaoUser:
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.email_verified = kwargs['email_verified']
        self.email = kwargs['email'] if 'email' in kwargs else None

        self.uname = kwargs['uname']
        self.picture = kwargs['picture']

    id: str
    email_verified: bool
    email: str

    uname: str
    picture: str
    birthday: str
    gender: str
