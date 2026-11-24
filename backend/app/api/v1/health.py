"""
Health check and platform status endpoints (L1 API).
"""
from fastapi import APIRouter
from app.config import settings

router = APIRouter()

@router.get("/health", tags=["Health"])
def health_check():
    """Verify application health and configuration status."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }

@router.get("/hello", tags=["Health"])
def legacy_hello():
    """Legacy hello world endpoint for backwards compatibility."""
    return {"message": "Hello, world!"}
