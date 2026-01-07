from pydantic import BaseModel
from typing import List

class AnalysisRequest(BaseModel):
    sentences: List[str]