from prometheus_client import CollectorRegistry, Counter, Gauge, push_to_gateway
import socket
from app.core.metrics import BaseMetrics
from app.core.config import settings
import requests
import re

class PushgatewayMetrics(BaseMetrics):
    def __init__(self):
        self.registry = CollectorRegistry()
        self.tasks_processed = Counter('tasks_processed', 'Total tasks processed', registry=self.registry)
        self.tasks_failed = Counter('tasks_failed', 'Total tasks failed', registry=self.registry)
        self.tasks_retried = Counter('tasks_retried', 'Total tasks retried', registry=self.registry)
        self.tasks_succeeded = Counter('tasks_succeeded', 'Total tasks succeeded', registry=self.registry)
        self.active_workers = Gauge('active_workers', 'Active workers', registry=self.registry)
        self.idle_workers = Gauge('idle_workers', 'Idle workers', registry=self.registry)
        self.queue_length = Gauge('queue_length', 'Queue length', registry=self.registry)
        self.pushgateway_addr = f"http://{settings.PROMETHEUS_PUSHGATEWAY_HOST}:{settings.PROMETHEUS_PUSHGATEWAY_PORT}" 
        self.job = f"zest-worker-{socket.gethostname()}"

    def push(self):
        push_to_gateway(self.pushgateway_addr, job=self.job, registry=self.registry)

    def task_succeeded(self):
        self.tasks_processed.inc()
        self.tasks_succeeded.inc()
        self.push()

    def task_failed(self):
        self.tasks_failed.inc()
        self.push()

    def task_retried(self):
        self.tasks_retried.inc()
        self.push()

    def set_queue_length(self, length: int):
        self.queue_length.set(length)
        self.push()

    def set_worker_counts(self, active: int, idle: int):
        self.active_workers.set(active)
        self.idle_workers.set(idle)
        self.push()

    def task_started(self):
        self.active_workers.inc()
        self.push()

    def get_statistics(self) -> dict:
        """
        Fetches and parses metrics from the Pushgateway's /metrics endpoint.
        Returns a dict with the global values for your metrics.
        """
        try:
            resp = requests.get(f"{self.pushgateway_addr}/metrics")
            resp.raise_for_status()
            text = resp.text
        except Exception as e:
            return {"error": f"Failed to fetch metrics from Pushgateway: {e}"}

        def extract_metric(name):
            # Find the first matching metric line (without labels)
            match = re.search(rf'^{name}(\{{.*\}})?\s+([0-9.eE+-]+)', text, re.MULTILINE)
            return int(float(match.group(2))) if match else 0

        return {
            "tasks_processed": extract_metric("tasks_processed_total"),
            "tasks_retried": extract_metric("tasks_retried_total"),
            "tasks_succeeded": extract_metric("tasks_succeeded_total"),
            "tasks_failed": extract_metric("tasks_failed_total"),
            "queue_length": extract_metric("queue_length"),
            "idle_workers": extract_metric("idle_workers"),
            "active_workers": extract_metric("active_workers"),
            "source": "pushgateway"
        }

    def reset(self):
        # Not supported for Prometheus counters
        pass