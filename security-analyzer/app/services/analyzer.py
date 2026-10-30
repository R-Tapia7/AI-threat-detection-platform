import pandas as pd
from app.models.log_models import SecurityLog, AnalysisResult
from app.services.threat_rules import *

import logging
from app.db.db_models import save_result_to_db
from sqlalchemy.orm import Session
from queue import Full
from app.store import results_store, logs_history, ai_queue

logger = logging.getLogger(__name__)

def analyze_logs(logs : list[SecurityLog], db: Session) -> list[AnalysisResult]:
    # Function that processes the incoming batch of logs and applies security rules

    # Add the new logs to our sliding history window
    logs_history.extend(logs)

    df = pd.DataFrame([log.model_dump() for log in logs_history])
    # Ensure the timestamp column is treated as real dates/times for mathematical operations
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    results = []

    for log in logs:
        threat_level = "SAFE" # Default state is safe
        rule_triggered = None

        # Check the rules one by one. Critical rules must come first
        if rule_brute_force(df, log.ip):
            threat_level = "CRITICAL"
            rule_triggered = "BRUTE_FORCE"

        else:
            triggered, level = rule_sensitive_resource(log)
            if triggered:
                threat_level = level
                rule_triggered = f"SENSITIVE_RESOURCE: {log.action} on {log.resource}"

            elif rule_mass_download(df, log.userId):
                threat_level = "SUSPICIOUS"
                rule_triggered = "MASS_DOWNLOAD"

            elif rule_off_hours(log):
                threat_level = "SUSPICIOUS"
                rule_triggered = "OFF_HOURS"

            elif rule_high_error_rate(df):
                threat_level = "SUSPICIOUS"
                rule_triggered = "HIGH_ERROR_RATE"

        result = AnalysisResult(
            logId=log.logId,
            timestamp=log.timestamp,
            ip=log.ip,
            userId=log.userId,
            action=log.action,
            status=log.status,
            threat_level=threat_level,
            rule_triggered=rule_triggered,
            ai_report=None      # filled in later by the worker
        )

        results.append(result)
        results_store.append(result)
        # Write to PostgreSQL immediately so it's safe even if Python crashes next
        save_result_to_db(db, result)

        # Enqueue only after the result exists in memory and in PostgreSQL,
        # so the worker is guaranteed to find it when it finishes.
        if threat_level != "SAFE" and rule_triggered:
            try:
                ai_queue.put_nowait((log, rule_triggered))
            except Full:
                logger.warning("AI queue full, skipping report for %s", log.logId)

    return results


    