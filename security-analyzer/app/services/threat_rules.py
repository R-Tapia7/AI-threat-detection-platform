from app.models.log_models import SecurityLog
import pandas as pd

# SECURITY RULES ENGINE
# These functions act as classical SIEM (Security Information 
# and Event Management) rules.

def rule_brute_force(df : pd.DataFrame, ip : str, window_minutes: int = 5) -> bool:
    """
    Checks if a specific IP has too many failed login attempts
    Filters the DataFrame for the given IP and status equals 'FAILURE'
    """
    cutoff = pd.Timestamp.now() - pd.Timedelta(minutes=window_minutes)

    failures = df[
        (df["ip"] == ip) &
        (df["status"] == "FAILURE") &
        (df["timestamp"] >= cutoff)
    ]
    
    return len(failures) > 10

def rule_off_hours(log : SecurityLog) -> bool:
    # Checks if the action was performed outside normal business hours (6 AM to 10 PM)
    hour = log.timestamp.hour
    return hour < 6 or hour > 22

def rule_sensitive_resource(log : SecurityLog) -> bool:
    # Triggers an alert if someone successfully accesses highly restricted areas
    critical_resources = ["/admin/panel", "/config/secrets"]
    critical_actions = ["ADMIN_ACCESS", "CONFIG_ACCESS"]
    if log.resource not in critical_resources or log.status != "SUCCESS":
        return False, ""

    if log.action in critical_actions:
        return True, "CRITICAL"
    else:
        # PASSWORD_CHANGE, DATA_EXPORT, FILE_DOWNLOAD on sensitive resources
        # are suspicious but not necessarily critical
        return True, "SUSPICIOUS"

def rule_mass_download(df : pd.DataFrame, user : str) -> bool:
    # Detects potential Data Exfiltration
    # Checks if the same user has downloaded files multiple times in this batch
    downloads = df[(df["userId"] == user) & (df["action"] == "FILE_DOWNLOAD")]
    return len(downloads) > 5

def rule_high_error_rate(df: pd.DataFrame, window_minutes: int = 5, threshold: float = 0.5) -> bool:
    """
    Detects an abnormally high ratio of FAILURE events system-wide
    in a short time window, could indicate a service under attack,
    a misconfiguration, or a credential stuffing campaign spread
    across multiple accounts instead of a single IP.
    """
    cutoff = pd.Timestamp.now() - pd.Timedelta(minutes=window_minutes)
    recent = df[df["timestamp"] >= cutoff]

    if len(recent) < 10:  # Not enough data yet to make a reliable judgment
        return False

    failure_ratio = len(recent[recent["status"] == "FAILURE"]) / len(recent)
    return failure_ratio > threshold
    