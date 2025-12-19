from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.request.context_request import ContextItem

class ScenarioResponse(BaseModel):
    id: str 
    name: str
    description: str
    contexts: List[ContextItem] 