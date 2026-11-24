"""Legacy redirect shim for app.fastapi.api."""
from app.api.v1.health import router

__all__ = ["router"]
