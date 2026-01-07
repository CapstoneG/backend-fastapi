from pydantic import BaseModel
from typing import List

class LearningDay(BaseModel):
    day: int
    focus: str
    goal: str
    example: str
    exercise_type: str

class RecommendationResponse(BaseModel):
    target_level: str
    top_weak_skills: List[str]
    learning_plan: List[LearningDay]
