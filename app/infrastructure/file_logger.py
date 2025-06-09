import os
from datetime import datetime
from filelock import FileLock
from app.core.logger import BaseLogger
from app.core.config import settings

class FileLogger(BaseLogger):
    def __init__(self):
        os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)

    def log(self, worker_id: str, task_id: str, message: str):
        log_entry = f"[{datetime.utcnow().isoformat()}] [Worker:{worker_id}] [Task:{task_id}] {message}\n"
        lock_path = f"{settings.LOG_FILE}.lock"
        
        with FileLock(lock_path):
            with open(settings.LOG_FILE, "a") as f:
                f.write(log_entry)