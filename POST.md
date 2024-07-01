---
title: AI Agent with Long Term Memory
date: "2024-06-18"
draft: true
description: How to Build an AI agent with long-term memory using Python & LangChain
---

# Building a Scalable FastAPI App with LangChain & LangGraph AI Agents

In this post, I'll guide you through the process of creating a FastAPI application. This app will serve three LangChain and LangGraph AI agents with long-term memory capabilities. The first agent answers questions, the second analyzes the responses for potential memories, and the third validates these memories before storing them in a database.

## Project Structure

We'll structure our project to be modular and maintainable. Here's an overview of the project structure:

```
langchain_app/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── langchain.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── memory.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── memory.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── base_service.py
│   │   ├── langchain_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── database.py
├── tests/
│   ├── __init__.py
│   ├── test_langchain.py
├── Dockerfile
├── requirements.txt
├── docker-compose.yml
└── README.md
```

## Setting Up FastAPI

Let's start by setting up our FastAPI application.

### Install Dependencies

Create a `requirements.txt` file and add the following dependencies:

```
fastapi
uvicorn
sqlalchemy
pydantic
langchain
langgraph
```

Then, install the dependencies:

```sh
pip install -r requirements.txt
```

### Application Configuration

Create a `config.py` file in the `core` directory to manage our application configuration:

```python
# app/core/config.py

from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    API_V1_STR: str = "/api/v1"

settings = Settings()
```

### Database Setup

Create a `database.py` file in the `utils` directory to handle our database connection:

```python
# app/utils/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

### Memory Model

Define a `Memory` model in the `models` directory to represent long-term memory entries:

```python
# app/models/memory.py

from sqlalchemy import Column, Integer, String, Text, Boolean
from app.utils.database import Base

class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True)
    response = Column(Text)
    long_term = Column(Boolean, default=False)
```

### Memory Schema

Create a `memory.py` file in the `schemas` directory to define Pydantic schemas:

```python
# app/schemas/memory.py

from pydantic import BaseModel

class MemoryBase(BaseModel):
    question: str
    response: str

class MemoryCreate(MemoryBase):
    long_term: bool

class Memory(MemoryBase):
    id: int

    class Config:
        orm_mode = True
```

### Abstract Service Class

Create a `base_service.py` file in the `services` directory for our abstract service class:

```python
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
```

### LangChain Service

Create a `langchain_service.py` file in the `services` directory to handle LangChain logic:

```python
# app/services/langchain_service.py

from langchain import LangChain
from app.models.memory import Memory
from app.schemas.memory import MemoryCreate
from app.utils.database import SessionLocal
from app.services.base_service import BaseService

class LangChainService(BaseService):
    def __init__(self):
        self.agent1 = LangChain()
        self.agent2 = LangChain(prompt="Analyze the response for potential memory.")
        self.agent3 = LangChain(prompt="Confirm if the memory should be saved.")

    def ask_question(self, question: str):
        response = self.agent1.ask(question)
        analysis = self.analyze_response(question, response)
        if analysis:
            self.confirm_memory(analysis, question, response)
        return response

    def analyze_response(self, question: str, response: str):
        return self.agent2.ask(f"Question: {question}
Response: {response}
Should this be remembered?")

    def confirm_memory(self, analysis: str, question: str, response: str):
        confirmation = self.agent3.ask(f"Analysis: {analysis}
Is this a valid memory?")
        if "yes" in confirmation.lower():
            self.save_memory(question, response, long_term=True)

    def save_memory(self, question: str, response: str, long_term: bool):
        db = SessionLocal()
        memory = Memory(question=question, response=response, long_term=long_term)
        db.add(memory)
        db.commit()
        db.refresh(memory)
        db.close()
        return memory
```

### API Endpoints

Create an `endpoints` directory and define our LangChain endpoints:

```python
# app/api/endpoints/langchain.py

from fastapi import APIRouter, Depends
from app.services.langchain_service import LangChainService
from app.schemas.memory import MemoryBase

router = APIRouter()

@router.post("/ask/")
def ask_question(question: MemoryBase, service: LangChainService = Depends()):
    response = service.ask_question(question.question)
    return {"response": response}
```

### Main Application

Wire everything together in the `main.py` file:

```python
# app/main.py

from fastapi import FastAPI
from app.core.config import settings
from app.api.endpoints import langchain
from app.utils.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(langchain.router, prefix=settings.API_V1_STR)
```

### Docker Setup

Create a `Dockerfile` and a `docker-compose.yml` file to containerize the application:

```Dockerfile
# Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml

version: "3.8"

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DATABASE_URL=sqlite:///./test.db
```

## Conclusion

By following this guide, you've set up a professional, modular, and scalable FastAPI application for serving an AI agents with long-term memory capabilities. This structure allows for easy maintenance and scalability as your project grows. Happy coding!
