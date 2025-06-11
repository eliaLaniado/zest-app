from app.core.config import settings
from app.core.consts import (
    LoggerType, MetricsType, QueueType,
    IMPLEMENTATION_REGISTRY, DEFAULT_LOGGER_TYPE,
    DEFAULT_METRICS_TYPE, DEFAULT_QUEUE_TYPE
)
from app.core.logger import BaseLogger
from app.core.metrics import BaseMetrics
from app.core.queue import BaseQueue
import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

def generic_factory(enum_type, setting_name, default_enum):
    raw_value = getattr(settings, setting_name, default_enum.value)
    try:
        enum_value = enum_type(raw_value)
    except ValueError:
        logger.warning(
            "Invalid %s value: %s. Using default: %s",
            enum_type.__name__,
            raw_value,
            default_enum.value
        )
        enum_value = default_enum

    try:
        impl_class = IMPLEMENTATION_REGISTRY[enum_type][enum_value]
        return impl_class()
    except KeyError:
        logger.error(
            "Missing implementation for %s.%s",
            enum_type.__name__,
            enum_value.value
        )
        raise RuntimeError(
            f"Configuration error: No implementation registered for {enum_value}"
        )

def logger_factory() -> BaseLogger:
    return generic_factory(LoggerType, "LOGGER_TYPE", DEFAULT_LOGGER_TYPE)

def metrics_factory() -> BaseMetrics:
    return generic_factory(MetricsType, "METRICS_TYPE", DEFAULT_METRICS_TYPE)

def queue_factory() -> BaseQueue:
    return generic_factory(QueueType, "QUEUE_TYPE", DEFAULT_QUEUE_TYPE)