"""Legacy redirect shim for app.users.api."""
from app.api.v1.users import router

__all__ = ["router"]
