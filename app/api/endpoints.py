from fastapi import APIRouter
from app.models.schema import SymptomInput
from app.services.reasoning import match_diseases
from app.services.llm import generate_summary

router = APIRouter()

@router.get('/status')
def root():
    return {'status': 'ok'}

@router.post("/match")
def match(input: SymptomInput):
    return match_diseases(input.text)

@router.post("/summary")
def summary(data: dict):
    return {"summary": generate_summary(data)}