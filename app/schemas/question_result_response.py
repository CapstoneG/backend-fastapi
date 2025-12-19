from pydantic import BaseModel
from typing import List, Dict, Optional

class QuestionResultResponse(BaseModel):
    question_id: str
    question_number: str
    user_answer: str
    correct_answer: str
    answer_text: list[str] = []
    question_text: Optional[str]
    transcript: Optional[str]
    transcript_clean: Optional[str]
    explanation: Optional[str]
    explanation_clean: Optional[str]
    is_correct: bool

