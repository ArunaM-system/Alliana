"""Legacy redirect shim for app.celery.api."""
from app.api.v1.tasks import router

__all__ = ["router"]
