# from logger import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import *


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
        
        

        # self.session.query(User).delete()
    
    def __exit__(self, type, value, traceback):
        self.session.close()
    

    def add_user(self, telegram_id, telegram_name, username, age, sex, info):
        try:
            if not bool(self.session.query(User).filter(User.telegram_id == telegram_id).first()):
                new_user = User(
                    telegram_id = telegram_id, 
                    telegram_name = telegram_name,
                    username = username,
                    age = age,
                    sex = sex,
                    info = info

                    )
                self.session.add(new_user)
                self.session.commit()
        except Exception as ex:
           print(ex)

    # def add_user(self, telegram_id, telegram_name):
    #     try:
    #         if not bool(self.session.query(User).filter(User.telegram_id == telegram_id).first()):
    #             new_user = User(
    #                 telegram_id = telegram_id, 
    #                 telegram_name = telegram_name)
    #             self.session.add(new_user)
    #             self.session.commit()
    #     except Exception as ex:
    #        print(ex)

    # def add_user(self, user):
    #     try:
    #         if not bool(self.session.query(User).filter(User.telegram_id == user.telegram_id).first()):
    #             new_user = User(
    #                 telegram_id = user.telegram_id, 
    #                 tg_name = user.tg_name, 
    #                 username = user.username, 
    #                 age = user.age, 
    #                 info = user.info, 
    #                 state = user.state)
    #             self.session.add(new_user)
    #             self.session.commit()
    #     except Exception as ex:
    #        print(ex)

    def update_user(self, telegram_id, username, age, sex, info):
        update_user = self.session.query(User).filter(User.telegram_id == telegram_id).first()
        if update_user:
            update_user.username = username,
            update_user.age = age,
            update_user.sex = sex,
            update_user.sex = info
            self.session.commit()

    # def update_user(self, user):
    #     update_user = self.session.query(User).filter(User.telegram_id == user.telegram_id).first()
    #     if update_user:
    #         update_user.username = user.username
    #         update_user.age = user.age
    #         update_user.info = user.info
    #         update_user.state = user.state
    #         self.session.commit()
    
    def update_state_user(self, telegram_id, state):
        user = self.session.query(User).filter(User.telegram_id == telegram_id).first()
        if user:
            user.state = state                
            self.session.commit()
    
    def update_conversation_with(self, telegram_id, conversation_with):
        user = self.session.query(User).filter(User.telegram_id == telegram_id).first()
        if user:
            user.conversation_with = conversation_with
            self.session.commit()

    def update_username(self, telegram_id, name):
        user = self.session.query(User).filter(User.telegram_id == telegram_id).first()
        if user:
            user.username = name
            self.session.commit()
    
    def update_age(self, telegram_id, age):
        user = self.session.query(User).filter(User.telegram_id == telegram_id).first()
        if user:
            user.age = age
            self.session.commit()
    

    def delete_user(self, user):
        user = self.session.query(User).filter(User.telegram_id == user.telegram_id).first()
        if user:
            self.session.delete(user)
            self.session.commit()


    
    

    def get_user_by_tid(self, telegram_id):
        return self.session.query(User).filter(User.telegram_id == telegram_id).first()
    
    def get_all_users(self):
        return self.session.query(User).all()
    def get_user_by_id(self, id):
        return self.session.query(User).filter(User.id == id).first()

    # def user_to_str(self, user : User) -> str:
    #     return (f"""{user.username}, {user.age} 
    #         \n{user.tg_name}
    #         \n{user.info}""")

db = ChatDB()
db.create_db()