from pydantic import BaseModel
from typing import List

class SymptomInput(BaseModel):
    text: str

class DiseaseMatch(BaseModel):
    name: str
    matches: int

class MatchResult(BaseModel):
    symptoms: List[str]
    diseases: List[DiseaseMatch]
