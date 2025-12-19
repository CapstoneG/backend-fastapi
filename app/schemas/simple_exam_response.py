from pydantic import BaseModel

class SimpleExamResponse(BaseModel):
    exam_id: str
    exam_title: str