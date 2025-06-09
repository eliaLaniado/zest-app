import redis
import pickle
from app.core.queue import BaseQueue
from app.domain.tasks import Task
from app.core.config import settings

class RedisQueue(BaseQueue):
    def __init__(self):
        self._redis = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=False
        )
        self._queue_name = settings.TASK_QUEUE_NAME

    def enqueue(self, task: Task) -> str:
        serialized = pickle.dumps(task)
        self._redis.lpush(self._queue_name, serialized)
        return str(task.id)

    def dequeue(self) -> Task:
        _, serialized = self._redis.brpop(self._queue_name)
        return pickle.loads(serialized)

    def get_queue_length(self) -> int:
        return self._redis.llen(self._queue_name)