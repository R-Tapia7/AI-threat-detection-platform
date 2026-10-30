# app/services/ai_worker.py

import logging
import threading

from app.db.database import SessionLocal
from app.db.db_models import AnalysisResultDB
from app.services.ai_reporter import get_ai_report
from app.store import ai_queue, results_store

logger = logging.getLogger(__name__)


def _worker_loop():
    # Runs forever in its own thread. queue.get() BLOCKS (sleeps) until
    # an item arrives, so it uses no CPU while the queue is empty.
    while True:
        log, rule_triggered = ai_queue.get()
        try:
            try:
                report = get_ai_report(log, rule_triggered)
            except Exception as e:
                # If Ollama is down or times out, we don't lose anything:
                # the log was already saved by the rule engine.
                logger.error("Ollama failed for %s: %s", log.logId, e)
                report = f"AI report unavailable: {e}"

            # 1. Update the in-memory result the dashboard reads.
            # list() takes a snapshot so the API thread can keep appending
            # to the deque while we search it.
            for result in list(results_store):
                if result.logId == log.logId:
                    result.ai_report = report
                    break

            # 2. Update the row in PostgreSQL. The worker is not inside an
            # HTTP request, so it can't use FastAPI's get_db(): it opens
            # and closes its own session.
            db = SessionLocal()
            try:
                db.query(AnalysisResultDB) \
                  .filter(AnalysisResultDB.log_id == log.logId) \
                  .update({"ai_report": report})
                db.commit()
            except Exception as e:
                db.rollback()
                logger.error("Could not save AI report to DB: %s", e)
            finally:
                db.close()

            logger.info("AI report ready for %s (%s)", log.ip, rule_triggered)
        finally:
            ai_queue.task_done()


def start_worker():
    # daemon=True means this thread dies automatically when the main
    # program exits, so it never keeps the server from shutting down.
    thread = threading.Thread(target=_worker_loop, daemon=True, name="ai-worker")
    thread.start()