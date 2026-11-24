"""Authentication and identity endpoints placeholder (L1 API)."""
from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/status")
def auth_status():
    return {"authenticated": False, "message": "Auth endpoints will be implemented in subsequent phases."}
