# app/services/base_service.py

from abc import ABC, abstractmethod

class BaseService(ABC):
    @abstractmethod
    def ask_question(self, question: str):
        pass

    @abstractmethod
    def analyze_response(self, question: str, response: str):
        pass

    @abstractmethod
    def confirm_memory(self, analysis: str):
        pass