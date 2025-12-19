from pydantic import BaseModel
from typing import Optional, List
from app.schemas.error_analysis import ErrorAnalysis

class ConversationResponse(BaseModel):
    response: str
    analysis: Optional[ErrorAnalysis] = None
    alternatives: List[str] = []
    translation: Optional[str] = None