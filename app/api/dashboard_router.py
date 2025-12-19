from fastapi import APIRouter
from app.services.sentence_service import SentenceService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
service = SentenceService()

@router.get("/topics")
def get_topics():
    return service.get_topics()

@router.get("/levels")
def get_levels():
    return service.get_levels()

@router.get("/sets")
def get_sets():
    return service.get_sets()