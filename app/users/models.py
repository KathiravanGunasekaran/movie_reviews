from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql.expression import text
from ..database import base


class User(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)
