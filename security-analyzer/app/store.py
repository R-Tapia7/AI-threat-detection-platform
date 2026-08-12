from app.models.log_models import AnalysisResult, SecurityLog
from collections import deque

results_store: deque[AnalysisResult] = deque(maxlen=200)

# This needs to hold more logs than results_store because
# brute force / mass download need to look back further in time
# than a single batch of 5 logs.
logs_history: deque[SecurityLog] = deque(maxlen=500)