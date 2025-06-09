from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    message: str
    attempts: int = 0