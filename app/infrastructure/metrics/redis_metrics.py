import redis
from app.core.metrics import BaseMetrics
from app.core.config import settings

class RedisMetrics(BaseMetrics):
    def __init__(self):
        self._redis = redis.Redis(host=settings.REDIS_HOST, port=6379, db=0)
        self._prefix = "metrics:"

    def task_started(self):
        self._redis.incr(f"{self._prefix}active_workers")
    
    def task_processed(self):
        self._redis.incr(f"{self._prefix}tasks_processed")

    def task_succeeded(self):
        self._redis.incr(f"{self._prefix}tasks_succeeded")
        self._redis.decr(f"{self._prefix}active_workers")

    def task_failed(self):
        self._redis.incr(f"{self._prefix}tasks_failed")
        self._redis.decr(f"{self._prefix}active_workers")

    def task_retried(self):
        self._redis.incr(f"{self._prefix}tasks_retried")

    def set_queue_length(self, length: int):
        self._redis.set(f"{self._prefix}queue_length", length)

    def set_worker_counts(self, active: int, idle: int):
        self._redis.set(f"{self._prefix}active_workers", active)
        self._redis.set(f"{self._prefix}idle_workers", idle)

    def get_statistics(self) -> dict:
        keys = [
            "tasks_processed", "tasks_retried", "tasks_succeeded", "tasks_failed",
            "queue_length", "idle_workers", "active_workers"
        ]
        stats = {}
        for key in keys:
            value = self._redis.get(f"{self._prefix}{key}")
            stats[key] = int(value) if value else 0
        return stats

    def reset(self):
        keys = [
            "tasks_processed", "tasks_retried", "tasks_succeeded", "tasks_failed",
            "queue_length", "idle_workers", "active_workers"
        ]
        for key in keys:
            self._redis.set(f"{self._prefix}{key}", 0)