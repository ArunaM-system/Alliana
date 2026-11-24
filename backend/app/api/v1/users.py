"""
Users endpoints (L1 API).
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict

from app.core.dependencies import get_db
from app.database.models.user import User

class UserOut(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)

router = APIRouter()

@router.get("/", response_model=List[UserOut], tags=["Users"])
def list_users(db: Session = Depends(get_db)):
    """Retrieve all users."""
    return db.query(User).all()
