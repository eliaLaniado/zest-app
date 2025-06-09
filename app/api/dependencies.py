from app.core.factories import logger_factory, metrics_factory, queue_factory
from app.core.logger import BaseLogger
from app.core.metrics import BaseMetrics
from app.core.queue import BaseQueue

def get_logger() -> BaseLogger:
    return logger_factory()

def get_metrics() -> BaseMetrics:
    return metrics_factory()

def get_queue() -> BaseQueue:
    return queue_factory()