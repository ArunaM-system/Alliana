"""Legacy redirect shim for app.users.crud."""
from sqlalchemy.orm import Session
from app.database.models.user import User

def get_all_users(db: Session):
    return db.query(User).all()
