# AI Agent with Long-Term Memory

This project demonstrates how to build a scalable FastAPI application that serves LangChain and LangGraph AI agents with long-term memory capabilities. The application includes three main agents: one for answering questions, one for analyzing responses for potential memories, and one for validating and storing these memories in a database.

## Table of Contents

- [AI Agent with Long-Term Memory](#ai-agent-with-long-term-memory)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Setting Up The App](#setting-up-the-app)
    - [Install Dependencies](#install-dependencies)
    - [Application Configuration](#application-configuration)
  - [Docker Setup](#docker-setup)
  - [Conclusion](#conclusion)

## Project Structure

The project is organized as follows:

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

## Setting Up The App

### Install Dependencies

Create a `requirements.txt` file with the following dependencies:

```
fastapi
uvicorn
sqlalchemy
pydantic
langchain
langgraph
```

Install the dependencies using:

```sh
pip install -r requirements.txt
```

### Application Configuration

Check the `config.py` file in the `core` directory for managing the application configuration:

```python
# app/core/config.py

from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    API_V1_STR: str = "/api/v1"

settings = Settings()
```

## Docker Setup

Create a `Dockerfile`:

```Dockerfile
# Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create a `docker-compose.yml` file:

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

By following this guide, you have set up a professional, modular, and scalable FastAPI application for serving AI agents with long-term memory capabilities. This structure allows for easy maintenance and scalability as your project grows. Happy coding!
