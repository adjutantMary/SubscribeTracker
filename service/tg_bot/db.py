from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, BigInteger, create_engine
import os

Base = declarative_base()

class User(Base):
    __tablename__ = 'users_customuser'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    phone = Column(String, unique=True)
    telegram_id = Column(BigInteger)

DB_URL = os.getenv("DB_URL")  # Пример: "postgresql://postgres:postgres@db:5432/postgres"
engine = create_engine(DB_URL)
