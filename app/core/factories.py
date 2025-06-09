from app.core.config import settings
from app.infrastructure.file_logger import FileLogger
from app.infrastructure.redis_metrics import RedisMetrics
from app.infrastructure.redis_queue import RedisQueue
from app.infrastructure.redis_priority_queue import RedisPriorityQueue
from app.core.logger import BaseLogger
from app.core.metrics import BaseMetrics
from app.core.queue import BaseQueue

def logger_factory() -> BaseLogger:
    if settings.LOGGER_TYPE == "file":
        return FileLogger()
    # Add other logger implementations here
    return FileLogger()

def metrics_factory() -> BaseMetrics:
    if settings.METRICS_TYPE == "redis":
        return RedisMetrics()
    # Add other metrics implementations here
    return RedisMetrics()

def queue_factory() -> BaseQueue:
    if settings.QUEUE_TYPE == "redis":
        return RedisQueue()
    if settings.QUEUE_TYPE == "redis_priority":
        return RedisPriorityQueue()
    # Add other queue implementations here
    return RedisQueue()