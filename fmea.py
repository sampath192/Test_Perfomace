import pandas as pd

DEFAULT_CSV = """
function,failure_mode,effect,mitigation_test
Wi-Fi communication,Doesn't reconnect after AP dropout,Data backlog -> stale/duplicate records,Simulate network outage; assert reconnect <30s
Touchscreen input,Touch events mis-registered under humidity stress,Wrong dosage entry,Run humidity chamber script; verify accuracy <5px
Battery charging,Stops charging above 80% after 1 year of cycles,Reduced runtime -> shutdown,Battery cycle 0-100% 1000x; check capacity >90%
Cloud sync,Fails to send payload under load,Lost dose history,Mock server under CPU load; assert no 5xx errors
Dose tracking,Misses duplicate-filtering on rapid events,Duplicate alarms,Fire two events <1s apart; expect one log entry
"""

def load_fmea(csv_path: str = None) -> pd.DataFrame:
    """
    Load FMEA table from a CSV file or use default template.
    """
    if csv_path:
        return pd.read_csv(csv_path)
    else:
        from io import StringIO
        return pd.read_csv(StringIO(DEFAULT_CSV))
        