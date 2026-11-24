"""
ALLINA Backend Application Entry Point.
FastAPI application configured with CORS, routing, and lifecycle hooks.
"""
import os
import sys

# Ensure backend root directory is in sys.path for reliable module resolution in all IDEs and runners
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from typing import List
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import settings
from app.api.v1.router import api_v1_router
from app.api.v1.users import UserOut
from app.database.models.user import User
from app.core.dependencies import get_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="ALLINA: Multi-Tenant AI-Powered IT Operations Platform",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Governed CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# L1: Mount versioned API routes under /api/v1
app.include_router(api_v1_router, prefix="/api/v1")

# Backwards compatibility legacy endpoints for existing frontend
@app.get("/hello", tags=["Legacy"])
def legacy_hello():
    return {"message": "Hello, world!"}

@app.get("/users/", response_model=List[UserOut], tags=["Legacy"])
def legacy_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/run-task", tags=["Legacy"])
def legacy_tasks():
    from app.celery.tasks import add
    task = add.delay(8, 20)
    return {"status": task.status, "task_id": str(task.id), "result": None}
