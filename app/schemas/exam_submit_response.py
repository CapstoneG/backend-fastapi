from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from app.schemas.group_result_response import GroupResultResponse
from app.schemas.question_result_response import QuestionResultResponse

class ExamSubmitResponse(BaseModel):
    is_full_test: bool      
    total_correct: int
    total_wrong: int
    total_skipped: int
    total_questions: int

    score: int = 0              
    listening_score: int = 0
    reading_score: int = 0
    
    details: List[QuestionResultResponse]