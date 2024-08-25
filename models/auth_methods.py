from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import INTEGER, BOOLEAN
from sqlalchemy.orm import relationship

from sql.database import Base


class AuthMethods(Base):
    def __init__(self, uuid: int, google: bool, kakao: bool, password: bool):
        self.uuid = uuid
        self.google = google
        self.kakao = kakao
        self.password = password

    __tablename__ = "auth_methods"
    __table_args__ = {"schema": "authentication"}

    uid = Column(INTEGER, primary_key=True, index=True, unique=True, nullable=False, autoincrement=True)
    uuid = Column(INTEGER, ForeignKey("users.users.uid"), unique=True, nullable=False)

    google = Column(BOOLEAN, nullable=False, default=False)
    kakao = Column(BOOLEAN, nullable=False, default=False)
    password = Column(BOOLEAN, nullable=False, default=False)

    user = relationship("User", back_populates="auth_methods")

    google_method = relationship("GoogleMethod", back_populates="auth_methods", uselist=False)
