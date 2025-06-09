import os
import threading
import time
import logging
import redis
from app.core.queue import BaseQueue
from app.core.logger import BaseLogger
from app.core.metrics import BaseMetrics
from app.worker.processor import TaskProcessor
from app.core.config import settings

logger = logging.getLogger(__name__)

class WorkerManager:
    def __init__(
        self,
        queue: BaseQueue,
        logger: BaseLogger,
        metrics: BaseMetrics
    ):
        self.queue = queue
        self.logger = logger
        self.metrics = metrics
        self.max_workers = os.cpu_count() or 4
        self.workers: list[threading.Thread] = []
        self.active = True
        self.active_workers = 0
        self.idle_workers = 0

    def start(self):
        logger.info(f"Starting worker pool with {self.max_workers} workers")
        for i in range(self.max_workers):
            logger.debug(f"Spawning worker thread {i+1}/{self.max_workers}")
            worker = threading.Thread(target=self._worker_loop, name=f"WorkerThread-{i+1}")
            worker.daemon = True
            worker.start()
            self.workers.append(worker)
            self.idle_workers += 1
        logger.info(f"All {self.max_workers} worker threads started.")

    def _worker_loop(self):
        thread_name = threading.current_thread().name
        logger.info(f"{thread_name} started.")
        last_activity = time.time()
        
        while self.active:
            try:
                logger.debug(f"{thread_name} waiting for task...")
                task = self.queue.dequeue()
                if task is None:
                    logger.debug(f"{thread_name} found no task in queue, sleeping briefly.")
                    time.sleep(0.1)
                    continue
                logger.info(f"{thread_name} dequeued task: {getattr(task, 'id', repr(task))}")
                self.idle_workers -= 1
                self.active_workers += 1
                
                processor = TaskProcessor(self.logger, self.metrics)
                logger.debug(f"{thread_name} processing task: {getattr(task, 'id', repr(task))}")
                success, processing_time = processor.process(task)
                if not success and task.attempts < settings.TASK_MAX_RETRIES:
                    logger.warning(
                        f"{thread_name} failed to process task {getattr(task, 'id', repr(task))}, "
                        f"retrying (attempt {task.attempts}/{settings.TASK_MAX_RETRIES})"
                    )
                    self.metrics.task_retried()
                    time.sleep(settings.TASK_ERROR_RETRY_DELAY)
                    self.queue.enqueue(task, priority=settings.RETRY_TASK_PRIORITY)
                elif not success:
                    logger.error(
                        f"{thread_name} permanently failed task {getattr(task, 'id', repr(task))} "
                        f"after {task.attempts} attempts. Dropping task."
                    )
                else:
                    logger.info(
                        f"{thread_name} successfully processed task {getattr(task, 'id', repr(task))} "
                        f"in {processing_time:.2f}s"
                    )
                
                self.active_workers -= 1
                self.idle_workers += 1
                last_activity = time.time()
                
            except redis.exceptions.ConnectionError as e:
                logger.error(f"{thread_name} Redis connection error: {str(e)}")
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"{thread_name} Worker error: {str(e)}")
                current_time = time.time()
                idle_time = current_time - last_activity
                
                if idle_time > settings.WORKER_TIMEOUT:
                    logger.info(f"{thread_name} exiting due to timeout after {idle_time:.2f} seconds idle.")
                    break
                    
                time.sleep(0.1)
        
        self.idle_workers -= 1
        logger.info(f"{thread_name} exiting.")

    def stop(self):
        logger.info("Stopping worker manager")
        self.active = False
        for worker in self.workers:
            if worker.is_alive():
                logger.debug(f"Joining {worker.name}")
                worker.join(timeout=5.0)
        logger.info("All worker threads stopped.")