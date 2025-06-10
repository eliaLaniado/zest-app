from fastapi import APIRouter, Depends, status
from app.models.tasks import CreateTaskRequest, Task
from app.api.dependencies import get_queue, get_logger
from app.core.queue import BaseQueue
from app.core.logger import BaseLogger

router = APIRouter()

@router.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(
    request: CreateTaskRequest,
    queue: BaseQueue = Depends(get_queue),
    logger: BaseLogger = Depends(get_logger)
) -> dict:
    task = Task(message=request.message)
    logger.info(f"Enqueuing task: id={task.id} message='{task.message}' attempts={task.attempts}")
    task_id = queue.enqueue(task)
    logger.info(f"Task enqueued with ID: {task_id} to queue {getattr(queue, '_queue_name', type(queue).__name__)}")
    return {"id": task_id}
