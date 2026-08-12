from fastapi import APIRouter, Depends
from app.models.log_models import SecurityLog, AnalysisResult
from app.services.analyzer import analyze_logs
from app.store import results_store
from app.db.database import get_db
from sqlalchemy.orm import Session

# Group related endpoints under a common prefix.
router = APIRouter(prefix = "/analyze", tags = ["analysis"])

@router.post("/", response_model = list[AnalysisResult])
def analyze(logs : list[SecurityLog], db: Session = Depends(get_db)):
    # Receives a batch of logs and runs the analysis.
    return analyze_logs(logs, db)

@router.get("/results", response_model = list[AnalysisResult])
def get_results():
    # Returns the last 200 results, newest first.
    # React will call this every 3 seconds to update the dashboard.
    sorted_results = sorted(results_store, key=lambda r: r.timestamp, reverse=True)
    return sorted_results

@router.get("/health")
def health_check():
    # Check if the API is running and accessible.
    return {"status": "ok", "service" : "security-analyzer"}

