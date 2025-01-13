
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String



Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    tg_name = Column(String)
    username = Column(String)
    age = Column(Integer)
    info = Column(String)
    state = Column(Integer, default=0)
    

