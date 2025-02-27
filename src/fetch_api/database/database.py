from sqlalchemy.orm import Session

from src.fetch_api.database.settings import SessionLocal, init_db

init_db()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
