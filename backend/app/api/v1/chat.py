"""Conversational interface endpoints placeholder (L1 API)."""
from fastapi import APIRouter

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.get("/status")
def chat_status():
    return {"message": "Chat service endpoint will be connected to L2 Orchestrator in subsequent phases."}
