from app.models.log_models import AnalysisResult, SecurityLog
from collections import deque
from queue import Queue

results_store: deque[AnalysisResult] = deque(maxlen=200)

# This needs to hold more logs than results_store because
# brute force / mass download need to look back further in time
# than a single batch of 5 logs.
logs_history: deque[SecurityLog] = deque(maxlen=500)

# Thread-safe FIFO queue: one side (the API) puts items in, the other
# side (the worker thread) takes them out. Python's Queue handles all the
# locking for us, so two threads can use it at the same time safely.
# maxsize=100 protects memory: if Ollama is very slow and 100 reports
# are already waiting, we stop adding more instead of growing forever.
ai_queue: Queue = Queue(maxsize=100)