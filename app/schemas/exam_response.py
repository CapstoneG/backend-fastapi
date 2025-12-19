from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from app.schemas.group_response import GroupResponse

class ExamResponse(BaseModel):
    id: str
    exam_title: str
    parts: Dict[str, List[GroupResponse]]
    total_questions: int = 200
    duration_minutes: int = 120

    model_config={
        'populate_by_name': True
    }