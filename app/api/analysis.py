from fastapi import APIRouter
from app.schemas.request.analysis_request import AnalysisRequest
from app.schemas.analysis_response import AnalysisResponse
from app.services.sentence_analyzer import SentenceAnalyzer
from app.services.skill_evaluator import SkillEvaluator
from app.services.sentence_analyzer import SentenceAnalysis

router = APIRouter(prefix="/analysis", tags=["Analysis"])

analyzer = SentenceAnalyzer()
evaluator = SkillEvaluator()

@router.post("/start", response_model=SentenceAnalysis)
def analyze_conversation(req: AnalysisRequest):
    errors = analyzer.analyze(req.sentences)
    print("Errors detected:", errors)
    result = evaluator.evaluate(req.sentences, errors)
    return result
