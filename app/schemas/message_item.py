from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.schemas.error_analysis import ErrorAnalysis

class MessageItem(BaseModel):
    role: str 
    content: str
    timestamp: datetime
    analysis: Optional[ErrorAnalysis] = None 