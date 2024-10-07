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

    sex = Column(CHAR, nullable=False, default="N")
    email = Column(VARCHAR, nullable=False, unique=True)
    email_verified = Column(BOOLEAN, nullable=False, default=False)
    role: Role = Column(VARCHAR, nullable=False, default=Role.ROLE_USER)

    auth_methods = relationship("AuthMethods", back_populates="user", uselist=False)
