from pydantic import BaseModel
from typing import Dict
from app.enums.enum_error_type import ErrorType

class AnalysisResponse(BaseModel):
    total_sentences: int
    error_counts: Dict[ErrorType, int]
    grammar_error_rate: float
    grammar_score: int
    vocabulary_score: int
    estimated_cefr: str
