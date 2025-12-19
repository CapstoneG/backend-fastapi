from pydantic import BaseModel

class SentenceResponse(BaseModel):
    id: str
    text: str
    topic: str
    level: str
    audio_url: str