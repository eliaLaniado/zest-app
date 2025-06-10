# app/worker/processor.py
import time
import random
import uuid
from app.core.logger import BaseLogger
from app.core.metrics import BaseMetrics
from app.core.config import settings
from app.models.tasks import Task

class TaskProcessor:
    def __init__(self, logger: BaseLogger, metrics: BaseMetrics):
        self.logger = logger
        self.metrics = metrics
        self.worker_id = str(uuid.uuid4())

    def process(self, task: Task) -> tuple[bool, float]:
        self.metrics.task_started()
        task.attempts += 1
        start_time = time.time()
        try:
            self.logger.log(self.worker_id, str(task.id), task.message)
            time.sleep(settings.TASK_SIMULATED_DURATION)
            processing_time = time.time() - start_time
            if random.random() < settings.TASK_SIMULATED_ERROR_PERCENTAGE:
                raise RuntimeError("Simulated processing error")
            self.metrics.task_succeeded()
            return True, processing_time
        except Exception as e:
            self.logger.error(f"Task {task.id} failed: {str(e)}", exc_info=True)
            self.metrics.task_failed()
            return False, time.time() - start_time