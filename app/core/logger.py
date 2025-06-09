from abc import ABC, abstractmethod

class BaseLogger(ABC):
    @abstractmethod
    def log(self, worker_id: str, task_id: str, message: str):
        pass