from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.request.context_request import ContextItem

class ScenarioModel(BaseModel):
    id: str = Field(alias="_id")
    name: str
    description: str
    available_variants: List[str] = [] 
    contexts: List[ContextItem] 