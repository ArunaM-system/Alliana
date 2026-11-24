"""
Root main.py shim.
Maintains backwards compatibility for deployment runtimes executing `uvicorn main:app`.
"""
import os
import sys

# Ensure backend directory is in sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

try:
    from app.main import app
except ImportError:
    from backend.app.main import app  # type: ignore

__all__ = ["app"]
