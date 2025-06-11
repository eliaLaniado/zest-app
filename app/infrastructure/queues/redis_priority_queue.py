import redis
from app.core.queue import BaseQueue
from app.models.tasks import Task
from app.core.config import settings

class RedisPriorityQueue(BaseQueue):
    def __init__(self):
        self._redis = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=False
        )
        self._queue_name = settings.TASK_QUEUE_NAME
        self._dead_letter_queue = settings.DEAD_LETTER_QUEUE_NAME

    def enqueue(self, task: Task, priority: int = settings.TASK_PRIORITY) -> str:
        task_data = task.model_dump_json().encode('utf-8')
        self._redis.zadd(self._queue_name, {task_data: priority})
        return str(task.id)

    def dequeue(self) -> Task:
        # Atomically pop the highest priority task (lowest score)
        result = self._redis.zpopmin(self._queue_name, 1)
        if not result:
            return None
        task_data, _ = result[0]  # (member, score) tuple
        return Task.model_validate_json(task_data)

    def get_queue_length(self) -> int:
        return self._redis.zcard(self._queue_name)

    def enqueue_dead_letter(self, task: Task) -> str:
        task_data = task.model_dump_json().encode('utf-8')
        self._redis.lpush(self._dead_letter_queue, task_data)
        return str(task.id)