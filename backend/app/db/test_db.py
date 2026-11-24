"""Legacy test_db script redirecting to new database session."""
from app.database.session import SessionLocal
from sqlalchemy import text

def test_connection_and_query():
    try:
        db = SessionLocal()
        result = db.execute(text("SELECT 1")).scalar()
        print("Connected to database. Result:", result)
        db.close()
    except Exception as e:
        print("Database connection test:", e)

if __name__ == "__main__":
    test_connection_and_query()
