from fastapi import APIRouter, Depends, HTTPException
from app.models.schema import SymptomInput
from app.services.reasoning import match_diseases
from app.services.llm import generate_summary
from app.db.neo4j import get_driver

router = APIRouter()

@router.get('/status')
def root():
    return {'status': 'ok'}

@router.post("/match")
def match(input: SymptomInput, driver=Depends(get_driver)):
    return match_diseases(input.text, driver)

@router.post("/summary")
def summary(data: dict):
    return {"summary": generate_summary(data)}