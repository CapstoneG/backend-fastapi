from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.schemas.message_item import MessageItem

class ChatSession(BaseModel):
    id: str = Field(alias="_id")
    user_id: int
    variant_id: str
    scenario_id: str
    context_id: str
    created_at: datetime 
    updated_at: datetime
    messages: List[MessageItem] = []

    class Config:
        populate_by_name = True