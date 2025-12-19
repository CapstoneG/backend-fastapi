from pydantic import BaseModel
from app.schemas.group_content_response import GroupContentResponse
from app.schemas.question_response import QuestionResponse

class GroupResponse(BaseModel):
    group_content: GroupContentResponse
    questions: list[QuestionResponse]