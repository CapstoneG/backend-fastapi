from fastapi import APIRouter
from app.schemas.recommendation import RecommendationResponse
from app.services.prompt_builder import PromptBuilder
from app.services.llm_client import LLMClient

router = APIRouter(prefix="/recommendation", tags=["Recommendation"])

prompt_builder = PromptBuilder()
llm_client = LLMClient()

@router.post("/", response_model=RecommendationResponse)
def recommend(skill_summary: dict):
    prompt = prompt_builder.build(skill_summary)
    ai_result = llm_client.generate(prompt)
    return ai_result
