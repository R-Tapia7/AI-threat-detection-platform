from sqlalchemy import Column, String, Integer, DateTime
from app.db.database import Base
import uuid
from app.models.log_models import AnalysisResult
from datetime import datetime

class AnalysisResultDB(Base):
    """
    This class represents a table in PostgreSQL.
    Each class attribute becomes a column.
    SQLAlchemy translates this into:
    CREATE TABLE analysis_results (...)
    """
    __tablename__ = "analysis_results"

    # Primary key — a unique identifier for each row.
    # We use a string UUID instead of an auto-incrementing integer
    # because it matches the logId we already generate in Java.
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    log_id = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    ip = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    action = Column(String, nullable=False)
    status = Column(String, nullable=False)
    threat_level = Column(String, nullable=False)
    rule_triggered = Column(String, nullable=True)   # nullable because SAFE logs have none
    ai_report = Column(String, nullable=True)         # nullable because not every threat gets an AI report
    created_at = Column(DateTime, nullable=False)

def save_result_to_db(db, result: AnalysisResult):
    """
    Converts a Pydantic AnalysisResult into a SQLAlchemy AnalysisResultDB
    and persists it. This is the manual conversion step mentioned earlier —
    Pydantic and SQLAlchemy models don't talk to each other automatically.
    """
    db_result = AnalysisResultDB(
        log_id=result.logId,
        timestamp=result.timestamp,
        ip=result.ip,
        user_id=result.userId,
        action=result.action,
        status=result.status,
        threat_level=result.threat_level,
        rule_triggered=result.rule_triggered,
        ai_report=result.ai_report,
        created_at=datetime.now()
    )
    db.add(db_result)    # Stages the insert
    db.commit()           # Actually writes it to PostgreSQL