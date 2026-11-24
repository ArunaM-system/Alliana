"""System events and webhook intake endpoints placeholder (L1 API)."""
from fastapi import APIRouter

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("/")
def list_events():
    return {"events": [], "message": "Event intake endpoints will be connected in subsequent phases."}
