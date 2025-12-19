from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel
from typing import Annotated
from fastapi import Query, Path
import qrcode
from io import BytesIO
from fastapi.responses import StreamingResponse
from app.api.sentence_router import routes as sentence_routes
from app.api.dashboard_router import router as dashboard_router
from app.api.exam_router import router as exam_router
from app.api.conversation_router import router as conversation_router
from app.api.variant_router import router as variant_router

app = FastAPI()

app.include_router(sentence_routes)
app.include_router(dashboard_router)
app.include_router(exam_router)
app.include_router(conversation_router)
app.include_router(variant_router)
