from pydantic import BaseModel
from typing import Optional

class ErrorAnalysis(BaseModel):
    has_error: bool
    # Quan trọng: Topic để làm hệ gợi ý (VD: Past Tense, Preposition)
    topic: Optional[str] = None 
    corrected: Optional[str] = None
    explanation: Optional[str] = None