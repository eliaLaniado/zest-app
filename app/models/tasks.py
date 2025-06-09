# app/models/tasks.py
from uuid import UUID, uuid4
from pydantic import BaseModel

class Task(BaseModel):
    id: UUID = uuid4()
    message: str
    attempts: int = 0