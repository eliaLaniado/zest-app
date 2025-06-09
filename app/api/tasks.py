from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from app.domain.tasks import Task
from app.api.dependencies import get_queue
from app.core.queue import BaseQueue

router = APIRouter()

class CreateTaskRequest(BaseModel):
    message: str

@router.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(
    request: CreateTaskRequest,
    queue: BaseQueue = Depends(get_queue)
) -> dict:
    task = Task(message=request.message)
    print(f"Enqueuing task: {task}")
    task_id = queue.enqueue(task)
    print(f"Task enqueued with ID: {task_id} to queue {queue._queue_name}") 
    return {"id": task_id}
