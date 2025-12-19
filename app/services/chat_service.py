from app.repositories.chat_repository import ChatRepository
from app.schemas.request.create_session_request import CreateSessionRequest
from datetime import datetime

class ChatService:
    def __init__(self):
        self.repository = ChatRepository()

    def create_new_session(self, req: CreateSessionRequest):
        new_session = {
            "user_id": req.user_id,
            "variant_id": req.variant_id,
            "scenario_id": req.scenario_id,
            "context_id": req.context_id,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "messages": [] # Bắt đầu với mảng rỗng
        }

        result = self.repository.create_new_session(new_session=new_session)

        return {
            "status": "success",
            "session_id": str(result.inserted_id)
        }