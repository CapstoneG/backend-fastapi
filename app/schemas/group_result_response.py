from pydantic import BaseModel
from app.schemas.question_result_response import QuestionResultResponse
from app.schemas.group_content_response import GroupContentResponse

class GroupResultResponse(BaseModel):
    group_content: GroupContentResponse
    questions: list[QuestionResultResponse]