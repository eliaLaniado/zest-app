from app.core.config import settings
from app.infrastructure.file_logger import FileLogger
from app.infrastructure.prom_metrics import PrometheusMetrics
from app.infrastructure.redis_queue import RedisQueue
from app.core.logger import BaseLogger
from app.core.metrics import BaseMetrics
from app.core.queue import BaseQueue

def get_logger() -> BaseLogger:
    return FileLogger()

_METRICS = PrometheusMetrics()

def get_metrics() -> BaseMetrics:
    return _METRICS

def get_queue() -> BaseQueue:
    return RedisQueue()