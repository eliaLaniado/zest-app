from abc import ABC, abstractmethod
from app.domain.tasks import Task

class BaseQueue(ABC):
    @abstractmethod
    def enqueue(self, task: Task) -> str:
        pass

    @abstractmethod
    def dequeue(self) -> Task:
        pass

    @abstractmethod
    def get_queue_length(self) -> int:
        pass