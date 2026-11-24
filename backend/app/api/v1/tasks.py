"""
Background task endpoints (L1 API).
Dispatches asynchronous tasks to Celery worker without blocking the event loop.
"""
from fastapi import APIRouter
from app.celery.tasks import add

router = APIRouter()

@router.get("/run-task", tags=["Tasks"])
def run_task():
    """Trigger an async Celery task and return the task reference."""
    task = add.delay(8, 20)
    # Return immediately to avoid blocking FastAPI event loop; provide task id for polling
    return {
        "status": task.status,
        "task_id": str(task.id),
        "result": None
    }
