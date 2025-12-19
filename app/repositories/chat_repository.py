from app.db.mongodb import db

import datetime

class ChatRepository:
    def __init__(self):
        self.collection = db['chat_sessions']

    def create_new_session(self, new_session):
        return self.collection.insert_one(new_session)
