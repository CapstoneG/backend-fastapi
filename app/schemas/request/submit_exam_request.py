from pydantic import BaseModel
from typing import List, Dict

class SubmitExamRequest(BaseModel):
    exam_id: str
    parts: List[str]
    answers: Dict[str, str]