"""
Celery worker configuration for asynchronous background tasks.
Reads broker and backend URLs from central settings.
Includes clearly labelled MOCK fallback when Celery is not installed in the host runtime.
"""
from app.config import settings

try:
    from celery import Celery
    celery_app = Celery(
        "allina_tasks",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND
    )
    celery_app.autodiscover_tasks(["app.celery"])
except ImportError:
    # MOCK: CeleryFallback when celery package is absent from the host Python environment
    class _MockTaskResult:
        def __init__(self, task_id="mock-task-id-12345", status="QUEUED"):
            self.id = task_id
            self.status = status

    class _MockCelery:
        def task(self, func):
            def delay(*args, **kwargs):
                return _MockTaskResult()
            func.delay = delay
            return func

        def autodiscover_tasks(self, *args, **kwargs):
            pass

    celery_app = _MockCelery()
