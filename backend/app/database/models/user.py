"""User model for authentication and identity with tenant partitioning."""
from sqlalchemy import Column, Integer, String
from app.database.base import Base, TenantMixin

class User(Base, TenantMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
