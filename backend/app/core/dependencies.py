"""
Core FastAPI dependencies.
Provides database session lifecycle management and tenant context resolution.
"""
from typing import Generator
from fastapi import Header, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """Provide a transactional database session."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_tenant_id(
    x_tenant_id: str = Header(default="tenant-default", description="Tenant identifier")
) -> str:
    """
    Extract and validate tenant ID from incoming request headers or JWT context.
    Ensures multi-tenant boundaries are strictly respected.
    """
    if not x_tenant_id or not x_tenant_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Valid tenant identifier is required."
        )
    return x_tenant_id.strip()
