from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, TIMESTAMP, CHAR
from sqlalchemy.orm import relationship

from sql.database import Base


class PasswordMethod(Base):
    __tablename__ = "password_method"
    __table_args__ = {"schema": "authentication"}

    uid = Column(INTEGER, primary_key=True, index=True, unique=True, nullable=False, autoincrement=True)
    auid = Column(INTEGER, ForeignKey("authentication.auth_methods.uid"), nullable=False, unique=True)
    auth_methods = relationship("AuthMethods", back_populates="password_method")

    userid = Column(VARCHAR, nullable=False, unique=True)
    password = Column(CHAR, nullable=False)
    last_changed = Column(TIMESTAMP, nullable=False, default="now()")
    last_used = Column(TIMESTAMP)
