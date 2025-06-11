from abc import ABC, abstractmethod
from app.models.tasks import Task

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

    @abstractmethod
    def enqueue_dead_letter(self, task: Task) -> str:
        """Enqueue a failed task to the dead letter queue"""
        pass