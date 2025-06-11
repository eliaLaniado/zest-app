import redis
import pickle
from app.core.queue import BaseQueue
from app.models.tasks import Task
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
    
    def enqueue_dead_letter(self, task: Task) -> str:
        task_data = task.model_dump_json().encode('utf-8')
        self._redis.lpush(self._dead_letter_queue, task_data)
        return str(task.id)