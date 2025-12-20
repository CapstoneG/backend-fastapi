from app.db.mongodb import db
from typing import Optional
from bson import ObjectId
from app.schemas.error_analysis import ErrorAnalysis
from datetime import datetime
from app.schemas.chat_session import ChatSession

class ChatRepository:
    def __init__(self):
        self.collection = db['chat_sessions']

    def create_new_session(self, new_session):
        return self.collection.insert_one(new_session)

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Lấy chi tiết session để làm context cho AI"""
        try:
            doc = self.collection.find_one({"_id": ObjectId(session_id)})
            if not doc:
                return None
            doc["_id"] = str(doc["_id"])
            return ChatSession(**doc)
        except Exception:
            return None

    def add_user_message(self, session_id: str, content: str, analysis: Optional[ErrorAnalysis]):
        """
        Lưu tin nhắn của User kèm kết quả phân tích lỗi từ AI.
        Dùng $push để atomic update.
        """
        message_data = {
            "role": "user",
            "content": content,
            "timestamp": datetime.now(),
            # Convert Pydantic object sang dict nếu có
            "analysis": analysis.model_dump() if analysis else None
        }

        self.collection.update_one(
            {"_id": ObjectId(session_id)},
            {
                "$push": {"messages": message_data},
                "$set": {"updated_at": datetime.now()}
            }
        )

    def add_ai_message(self, session_id: str, content: str):
        """Lưu câu trả lời của AI"""
        message_data = {
            "role": "model",
            "content": content,
            "timestamp": datetime.now()
        }

        self.collection.update_one(
            {"_id": ObjectId(session_id)},
            {
                "$push": {"messages": message_data},
                "$set": {"updated_at": datetime.now()}
            }
        )