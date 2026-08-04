from sqlalchemy import Column, DateTime, Integer, String, JSON
from datetime import datetime

from app.database.base import Base


class UserModel(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    username = Column(String, unique=True)

    email = Column(String, unique=True)

    password_hash = Column(String)

    role = Column(String)