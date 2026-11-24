"""SQLAlchemy Declarative Base and multi-tenant mixins for ALLINA."""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class TenantMixin:
    """Mixin that enforces multi-tenant data partitioning and timestamps."""
    tenant_id = Column(String(64), nullable=False, default="default-tenant", index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
