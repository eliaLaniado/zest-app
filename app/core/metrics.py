from abc import ABC, abstractmethod

class BaseMetrics(ABC):
    @abstractmethod
    def task_started(self):
        pass

    @abstractmethod
    def task_succeeded(self):
        pass

    @abstractmethod
    def task_failed(self):
        pass

    @abstractmethod
    def task_retried(self):
        pass

    @abstractmethod
    def set_queue_length(self, length: int):
        pass

    @abstractmethod
    def set_worker_counts(self, active: int, idle: int):
        pass

    @abstractmethod
    def get_statistics(self) -> dict:
        pass