import os
import concurrent.futures
import threading
import time
import logging
import redis
from typing import Optional
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
        logger_component: BaseLogger,
        metrics: BaseMetrics,
        max_workers: Optional[int] = None
    ):
        self.queue = queue
        self.logger = logger_component
        self.metrics = metrics
        self.max_workers = max_workers or settings.WORKER_COUNT
        self.active = False
        self.lock = threading.Lock()
        self.active_workers = 0
        self.idle_workers = self.max_workers
        self.executor = None
        self.futures = []

    def start(self):
        """Start the worker pool with automatic thread resurrection"""
        logger.info(f"Starting worker pool with {self.max_workers} workers")
        self.active = True
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers,
            thread_name_prefix="Worker"
        )
        
        # Submit initial workers
        for _ in range(self.max_workers):
            if self.active:
                future = self.executor.submit(self._worker_loop)
                self.futures.append(future)
                future.add_done_callback(self._worker_done_callback)

    def _worker_done_callback(self, future):
        """Automatically restart workers that die unexpectedly"""
        if self.active and future.exception():
            logger.error(f"Worker died with error: {future.exception()}")
            # Remove the dead future
            self.futures.remove(future)
            # Start a new worker
            new_future = self.executor.submit(self._worker_loop)
            self.futures.append(new_future)
            new_future.add_done_callback(self._worker_done_callback)

    def stop(self):
        """Gracefully shutdown the worker pool"""
        logger.info("Stopping worker manager")
        self.active = False
        
        if self.executor:
            self.executor.shutdown(wait=True)
            self.futures.clear()
        
        logger.info("Worker manager stopped")

    def _worker_loop(self):
        """Individual worker loop - now managed by ThreadPoolExecutor"""
        thread_name = threading.current_thread().name
        logger.info(f"{thread_name} started")
        
        while self.active:
            try:
                task = self.queue.dequeue()
                if task is None:
                    time.sleep(0.5)
                    continue

                with self.lock:
                    self.idle_workers -= 1
                    self.active_workers += 1

                try:
                    self._process_task(task, thread_name)
                finally:
                    with self.lock:
                        self.active_workers -= 1
                        self.idle_workers += 1

            except Exception as e:
                logger.error(f"{thread_name} error: {str(e)}", exc_info=True)
                time.sleep(0.1)
        
        logger.info(f"{thread_name} exiting")

    def _process_task(self, task, thread_name):
        """Encapsulated task processing logic"""
        logger.info(f"{thread_name} processing: {getattr(task, 'id', repr(task))}")
        processor = TaskProcessor(self.logger, self.metrics)
        
        success, processing_time = processor.process(task)
        self.metrics.task_processed()
        
        if not success:
            if task.attempts < settings.TASK_MAX_RETRIES:
                logger.warning(
                    f"{thread_name} retrying {getattr(task, 'id', repr(task))} "
                    f"(attempt {task.attempts}/{settings.TASK_MAX_RETRIES})"
                )
                self.metrics.task_retried()
                time.sleep(settings.TASK_ERROR_RETRY_DELAY)
                self.queue.enqueue(task, priority=settings.RETRY_TASK_PRIORITY)
            else:
                logger.error(
                    f"{thread_name} moving task to dead letter queue: {getattr(task, 'id', repr(task))}"
                )
                self.queue.enqueue_dead_letter(task)
                self.metrics.task_dead_lettered()