from fastapi import APIRouter
from app.schemas.request.conversation_request import ChatRequest
from app.schemas.conversation_response import ConversationResponse
from app.schemas.request.create_session_request import CreateSessionRequest
from app.services.chat_service import ChatService

router = APIRouter(prefix="/conversation", tags=["Conversation"])
chat_service = ChatService()

@router.post('/check-health')
def check_health():
    return chat_service.check_health()

@router.post('/message', response_model=ConversationResponse)
def send_message(request: ChatRequest):
    return chat_service.process_chat_message(
        session_id=request.session_id,
        user_message=request.message
    )

@router.post('/session/create')
def create_new_session(request: CreateSessionRequest):
    return chat_service.create_new_session(req=request)