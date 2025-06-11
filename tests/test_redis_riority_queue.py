from app.infrastructure.queues.redis_priority_queue import RedisPriorityQueue
from unittest.mock import patch
import pytest

@pytest.fixture
def queue():
    with patch("redis.Redis") as mock_redis:
        yield RedisPriorityQueue()

def test_enqueue_and_dead_letter(queue, sample_task):
    # Enqueue task
    task_id = queue.enqueue(sample_task)
    assert task_id == str(sample_task.id)
    # Enqueue to dead letter
    task_id2 = queue.enqueue_dead_letter(sample_task)
    assert task_id2 == str(sample_task.id)