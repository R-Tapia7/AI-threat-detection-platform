# app/models/log_models.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# When FastAPI receives an HTTP request, the body arrives as JSON text.
# Pydantic automatically converts it into a Python object
# and validates that it has the correct fields.

class SecurityLog(BaseModel):
    logId: str
    timestamp: datetime
    ip: str
    userId: str
    action: str
    status: str
    attempts: int
    country: str
    resource: str

# This model defines the structure of the response we will send back or save.
class AnalysisResult(BaseModel):
    logId: str
    timestamp: datetime
    ip: str
    userId: str
    action: str
    status: str
    threat_level: str           # SAFE, SUSPICIOUS, CRITICAL
    rule_triggered: Optional[str] = None   # What rule triggered the alert
    ai_report: Optional[str] = None        # NLP explanation from the LLM