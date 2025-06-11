import logging
import os
from filelock import FileLock
from app.core.logger import BaseLogger
from app.core.config import settings

class FileLogger(BaseLogger):
    def __init__(self):
        os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)
        self.log_file = settings.LOG_FILE
        self.logger = logging.getLogger("FileLogger")
        if not self.logger.handlers:
            handler = logging.FileHandler(self.log_file)
            formatter = logging.Formatter(
                '[%(asctime)s] [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%dT%H:%M:%S'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def info(self, message: str):
        with FileLock(self.log_file + ".lock"):
            self.logger.info(message)

    def error(self, message: str, exc_info: bool = False):
        with FileLock(self.log_file + ".lock"):
            self.logger.error(message, exc_info=exc_info)

    def debug(self, message: str):
        with FileLock(self.log_file + ".lock"):
            self.logger.debug(message)

    def log(self, worker_id: str, task_id: str, message: str):
        self.info(f"[Worker:{worker_id}] [Task:{task_id}] {message}")

    def warning(self, message: str):
        with FileLock(self.log_file + ".lock"):
            self.logger.warning(message)