import time
import random
import uuid
import logging
from app.core.logger import BaseLogger
from app.core.metrics import BaseMetrics
from app.core.config import settings
from app.domain.tasks import Task

logger = logging.getLogger(__name__)

class TaskProcessor:
    def __init__(self, logger: BaseLogger, metrics: BaseMetrics):
        self.logger = logger
        self.metrics = metrics
        self.worker_id = str(uuid.uuid4())

    def process(self, task: Task):
        self.metrics.task_started()
        task.attempts += 1
        
        try:
            # Log the task
            self.logger.log(self.worker_id, str(task.id), task.message)
            
            # Simulate processing time
            start_time = time.time()
            time.sleep(settings.TASK_SIMULATED_DURATION)
            processing_time = time.time() - start_time
            
            # Simulate random failure
            if random.random() < settings.TASK_SIMULATED_ERROR_PERCENTAGE:
                raise RuntimeError("Simulated processing error")
                
            # Mark success
            self.metrics.task_succeeded()
            return True
            
        except Exception as e:
            logger.error(f"Task {task.id} failed: {str(e)}")
            if task.attempts < settings.TASK_MAX_RETRIES:
                self.metrics.task_retried()
                time.sleep(settings.TASK_ERROR_RETRY_DELAY)
                return False
            else:
                self.metrics.task_failed()
                return False