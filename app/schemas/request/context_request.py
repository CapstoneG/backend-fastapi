from typing import List, Optional
from pydantic import BaseModel, Field

class ContextItem(BaseModel):
    id: str
    name: str
    description: str
    initial_ai_message: str