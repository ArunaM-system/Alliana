"""Human approval workflow endpoints placeholder (L1 API)."""
from fastapi import APIRouter

router = APIRouter(prefix="/approvals", tags=["Approvals"])

@router.get("/")
def list_approvals():
    return {"approvals": [], "message": "Human approval endpoints will be connected to L5 Governance in subsequent phases."}
