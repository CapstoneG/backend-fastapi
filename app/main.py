from fastapi import FastAPI
from contextlib import asynccontextmanager

# Import Service
from app.services.lightrag_service import rag_service 

# Import các Router
from app.api.sentence_router import routes as sentence_routes
from app.api.dashboard_router import router as dashboard_router
from app.api.exam_router import router as exam_router
from app.api.conversation_router import router as conversation_router
from app.api.variant_router import router as variant_router
from app.api.chatbot_router import router as chatbot_router
from app.api.analysis import router as analysis_router
from app.api.recommendation import router as recommendation_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 System starting up...")
    await rag_service.initialize() #
    
    yield 
    
    print("🛑 System shutting down...")


app = FastAPI(lifespan=lifespan)

# --- 3. INCLUDE ROUTERS ---
app.include_router(sentence_routes)
app.include_router(dashboard_router)
app.include_router(exam_router)
app.include_router(conversation_router)
app.include_router(variant_router)
app.include_router(chatbot_router) 
app.include_router(analysis_router)
app.include_router(recommendation_router)

@app.get("/")
async def root():
    return {"message": "English App API is running"}