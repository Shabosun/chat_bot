
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String



Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    telegram_name = Column(String)
    username = Column(String)
    age = Column(Integer, default=0)
    sex = Column(String)
    info = Column(String )
    state = Column(Integer, default=0) #0 - free, 1 - busy
    conversation_with = Column(Integer, unique=True) 
    

