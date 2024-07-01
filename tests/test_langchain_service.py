import pytest
from unittest.mock import MagicMock
from app.services.langchain_service import LangChainService
from app.core.config import settings

@pytest.fixture
def langchain_service(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", settings.OPENAI_API_KEY)
    return LangChainService()

def test_ask_question(langchain_service):
    question = "What is the capital of France?"
    response = langchain_service.ask_question(question)
    assert isinstance(response, str)

def test_analyze_response(langchain_service):
    question = "What is the capital of France?"
    response = "The capital of France is Paris."
    analysis = langchain_service.analyze_response(question, response)
    assert isinstance(analysis, str)

def test_confirm_memory(langchain_service, monkeypatch):
    analysis = "Positive"
    question = "What is the capital of France?"
    response = "The capital of France is Paris."
    mock_save_memory = MagicMock()
    monkeypatch.setattr(langchain_service, "save_memory", mock_save_memory)
    langchain_service.confirm_memory(analysis, question, response)
    mock_save_memory.assert_called_with(question, response, long_term=True)

def test_save_memory(langchain_service):
    question = "What is the capital of France?"
    response = "The capital of France is Paris."
    memory = langchain_service.save_memory(question, response, long_term=True)
    assert memory.id is not None
    assert memory.question == question
    assert memory.response == response
    assert memory.long_term

def test_load_memory(langchain_service):
    query = "What is the capital of France?"
    memory_data = langchain_service.load_memory(query)
    assert isinstance(memory_data, dict)
