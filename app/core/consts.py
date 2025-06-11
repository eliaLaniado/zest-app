from enum import Enum
from app.infrastructure.loggers.file_logger import FileLogger
from app.infrastructure.metrics.redis_metrics import RedisMetrics
from app.infrastructure.metrics.pushgateway_metrics import PushgatewayMetrics
from app.infrastructure.queues.redis_queue import RedisQueue
from app.infrastructure.queues.redis_priority_queue import RedisPriorityQueue


class LoggerType(str, Enum):
    FILE = "file"

class MetricsType(str, Enum):
    REDIS = "redis"
    PUSHGATEWAY = "pushgateway"

class QueueType(str, Enum):
    REDIS = "redis"
    PRIORITY_REDIS = "redis_priority"

DEFAULT_LOGGER_TYPE = LoggerType.FILE
DEFAULT_METRICS_TYPE = MetricsType.PUSHGATEWAY
DEFAULT_QUEUE_TYPE = QueueType.REDIS

# Mapping registry
IMPLEMENTATION_REGISTRY = {
    LoggerType: {
        LoggerType.FILE: FileLogger,
    },
    MetricsType: {
        MetricsType.REDIS: RedisMetrics,
        MetricsType.PUSHGATEWAY: PushgatewayMetrics,
    },
    QueueType: {
        QueueType.REDIS: RedisQueue,
        QueueType.PRIORITY_REDIS: RedisPriorityQueue,
    }
}