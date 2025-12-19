from app.services.conversation_service import ConversationService
from fastapi import APIRouter
from app.schemas.request.conversation_request import ChatRequest
from app.schemas.conversation_response import ConversationResponse
from app.schemas.request.create_session_request import CreateSessionRequest
from app.services.chat_service import ChatService

router = APIRouter(prefix="/conversation", tags=["Conversation"])
conversation_service = ConversationService()
chat_service = ChatService()

@router.post('/check-health')
def check_health():
    return conversation_service.check_health()

@router.post('/message', response_model=ConversationResponse)
def send_message(request: ChatRequest):
    return 1

@router.post('/session/create')
def create_new_session(request: CreateSessionRequest):
    return chat_service.create_new_session(req=request)