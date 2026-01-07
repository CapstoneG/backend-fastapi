from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.chatbot_service import chatbot_service 
from app.services.lightrag_service import rag_service

# Khởi tạo router (chú ý prefix)
router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

# DTO
class ChatRequest(BaseModel):
    message: str
    mode: str = "hybrid"

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        response_text = await chatbot_service.process_question(user_message=request.message, history=[])
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API Ingest data
@router.post("/ingest")
async def ingest_document(text: str):
    try:
        await rag_service.insert_content(text)
        return {"status": "success", "message": "Đã nạp dữ liệu vào RAG"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))