# from logger import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *


class ChatDB:
    def __init__(self):
        self.engine = self.setup_database()
        self.session = self.get_session(self.engine)
    
    def setup_database(self, db_path="sqlite:///chat.db"):
        engine = create_engine(db_path)
        return engine

    def get_session(self, engine):
        Session = sessionmaker(bind=engine)
        return Session()

    def create_db(self):
        Base.metadata.create_all(self.engine)

        self.session.query(User).delete()
    

    def add_user(self, user):
        try:
            if not bool(self.session.query(User).filter(User.telegram_id == user.telegram_id).first()):
                new_user = User(telegram_id = user.telegram_id, tg_name = user.tg_name, username = user.username, age = user.age, info = user.info, state = user.state)
                self.session.add(new_user)
                self.session.commit()
        except Exception as ex:
           print(ex)

    def update_user(self, user):
        update_user = self.session.query(User).filter(User.telegram_id == user.telegram_id).first()
        if update_user:
            update_user.username = user.username
            update_user.age = user.age
            update_user.info = user.info
            update_user.state = user.state
            self.session.commit()

    def delete_user(self, user):
        user = self.session.query(User).filter(User.telegram_id == user.telegram_id).first()
        if user:
            self.session.delete(user)
            self.session.commit()

    def update_state_user(self, telegram_id, state):
        user = self.session.query(User).filter(User.telegram_id == telegram_id).first()
        if user:
            user.state = state
            self.session.commit()

    def get_user_by_tid(self, telegram_id):
        return self.session.query(User).filter(User.telegram_id == telegram_id).first()
        