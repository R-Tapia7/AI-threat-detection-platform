import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
# A session is a single conversation with the database — it tracks
# changes you make and lets you commit (save) or rollback (undo) them.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependency function for FastAPI. Creates a new session for each
    request, and guarantees it closes afterward — even if an error occurs.
    This pattern is called 'dependency injection' and FastAPI has
    native support for it.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
