from pydantic import BaseModel
from typing import Optional

class QuestionResponse(BaseModel):
    question_id: str
    question_number: str
    question_text: Optional[str]
    answer_quantity: int
    answer_text: list[str] = []
    correct_answer: str
