# app/api/endpoints/langchain.py

from fastapi import APIRouter, Depends
from app.services.langchain_service import LangChainService
from app.schemas.memory import MemoryBase

router = APIRouter()

@router.post("/ask/")
def ask_question(question: MemoryBase, service: LangChainService = Depends()):
    response = service.ask_question(question.question)
    return {"response": response}