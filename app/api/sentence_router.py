from fastapi import APIRouter
from app.services.sentence_service import SentenceService
from app.schemas.sentence_response import SentenceResponse

routes = APIRouter(prefix="/sentences", tags=["Sentences"])
service = SentenceService()

@routes.get("/", response_model=list[SentenceResponse])
def get_all_sentences():
    return service.get_all_sentences()

@routes.get("/level/{level}", response_model=list[SentenceResponse])
def get_sentences_by_level(level: str):
    return service.get_sentences_by_level(level)

@routes.get("/id/{sentence_id}", response_model=SentenceResponse)
def get_sentence_by_id(sentence_id: str):
    return service.get_sentence_by_id(sentence_id)

@routes.get("/topic/{topic}", response_model=list[SentenceResponse])
def get_sentences_by_topic(topic: str):
    return service.get_sentences_by_topic(topic)

@routes.post("/")
def create_sentence(sentence_data: dict):
    return service.create_sentence(sentence_data)

@routes.get("/topic/{topic}/level/{level}", response_model=list[SentenceResponse])
def get_sentences_by_topic_and_level(topic: str, level: str):
    return service.get_sentences_by_topic_and_level(topic, level)

@routes.get("/topic/level/{level}")
def get_topics_by_level(level: str):
    return service.get_topics_by_level(level)

@routes.get("/level/topic/{topic}")
def get_levels_by_topic(topic: str):
    return service.get_levels_by_topic(topic)

