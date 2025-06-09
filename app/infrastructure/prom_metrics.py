from prometheus_client import Counter, Gauge, Histogram
from app.core.metrics import BaseMetrics
from app.core.config import settings

class PrometheusMetrics(BaseMetrics):
    def __init__(self):
        self.tasks_processed = Counter('tasks_processed', 'Total tasks processed')
        self.tasks_retried = Counter('tasks_retried', 'Total task retries')
        self.tasks_succeeded = Counter('tasks_succeeded', 'Successful tasks')
        self.tasks_failed = Counter('tasks_failed', 'Failed tasks')
        self.queue_length = Gauge('queue_length', 'Current queue size')
        self.idle_workers = Gauge('idle_workers', 'Idle workers count')
        self.active_workers = Gauge('active_workers', 'Active workers count')
        self.processing_time = Histogram(
            'processing_time', 
            'Task processing latency',
            buckets=[0.1, 0.5, 1, 2, 5]
        )
        self._active_workers = 0
        self._idle_workers = 0

    def task_started(self):
        self.active_workers.inc()
        self._active_workers += 1

    def task_succeeded(self):
        self.tasks_processed.inc()
        self.tasks_succeeded.inc()
        self.active_workers.dec()
        self._active_workers -= 1

    def task_failed(self):
        self.tasks_failed.inc()
        self.active_workers.dec()
        self._active_workers -= 1

    def task_retried(self):
        self.tasks_retried.inc()

    def set_queue_length(self, length: int):
        self.queue_length.set(length)

    def set_worker_counts(self, active: int, idle: int):
        self.active_workers.set(active)
        self.idle_workers.set(idle)
        self._active_workers = active
        self._idle_workers = idle

    def get_statistics(self) -> dict:
        return {
            "processed": int(self.tasks_processed._value.get()),
            "retries": int(self.tasks_retried._value.get()),
            "succeeded": int(self.tasks_succeeded._value.get()),
            "failed": int(self.tasks_failed._value.get()),
            "avg_processing_time": self.processing_time._sum / self.tasks_processed._value.get() if self.tasks_processed._value.get() > 0 else 0,
            "queue_length": int(self.queue_length._value.get()),
            "idle_workers": self._idle_workers,
            "active_workers": self._active_workers
        }