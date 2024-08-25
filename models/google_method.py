from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, TIMESTAMP
from sqlalchemy.orm import relationship

from sql.database import Base


class GoogleMethod(Base):
    __tablename__ = "google_method"
    __table_args__ = {"schema": "authentication"}

    uid = Column(INTEGER, primary_key=True, index=True, unique=True, nullable=False, autoincrement=True)
    auid = Column(INTEGER, ForeignKey("authentication.auth_methods.uid"), nullable=False, unique=True)
    auth_methods = relationship("AuthMethods", back_populates="google_method")

    google_id = Column(VARCHAR, nullable=False, unique=True)
    last_used = Column(TIMESTAMP)
