import os
import httpx
from app.models.log_models import SecurityLog

# Ollama runs a local server on this URL automatically.
# No API key needed
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = "llama3.2"

def build_prompt(log : SecurityLog, rule_triggered : str) -> str:
    # Converts a suspicious log into a structured prompt for the LLM.
    return f"""You are a senior cybersecurity analyst at a corporate SOC (Security Operations Center).
A rule-based detection system has flagged the following event as suspicious.
Analyze it and generate a concise security report in English.

--- FLAGGED EVENT ---
User:        {log.userId}
IP Address:  {log.ip}
Country:     {log.country}
Action:      {log.action}
Resource:    {log.resource}
Status:      {log.status}
Timestamp:   {log.timestamp}
Rule fired:  {rule_triggered}
---------------------

Respond using EXACTLY this structure (keep the headers):

## Incident Summary
[2-3 sentences describing what happened]

## Risk Level
[CRITICAL / HIGH / MEDIUM — and one sentence explaining why]

## Probable Attack Technique
[Name the likely technique, e.g. Brute Force, Credential Stuffing, Data Exfiltration.
Reference the MITRE ATT&CK ID if applicable, e.g. T1110]

## Recommended Mitigation
[3 concrete, actionable steps]
"""

def get_ai_report(log : SecurityLog, rule_triggered : str) -> str:
    # Sends the prompt to the local Ollama server and returns the report.
    prompt = build_prompt(log, rule_triggered)

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False   # Wait for the full response before returning.
    }

    print(f"[Ollama] Sending request for {log.ip} | {rule_triggered}")

    # Plain synchronous call
    # timeout=120 because Llama 3.2 can take up to 60s on CPU.
    response = httpx.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()

    report = response.json()["response"]
    print(f"[Ollama] Report received for {log.ip}")
    return report
    
