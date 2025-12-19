from pydantic import BaseModel
from typing import Optional

class GroupContentResponse(BaseModel):
    audio_url: Optional[str] = None
    reading_text: Optional[str] = None
    reading_text_clean: Optional[str] = None
    image_url: list[str] = []
