from abc import ABC, abstractmethod

class BaseLogger(ABC):
    @abstractmethod
    def info(self, message: str):
        pass

    @abstractmethod
    def error(self, message: str, exc_info: bool = False):
        pass

    @abstractmethod
    def debug(self, message: str):
        pass

    @abstractmethod
    def log(self, worker_id: str, task_id: str, message: str):
        pass