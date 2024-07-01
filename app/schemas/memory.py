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