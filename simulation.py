import pandas as pd
import numpy as np
from datetime import datetime, timedelta

ERROR_TYPES = {
    "dose_event": "DoseMisfire",
    "reboot": "RebootError",
    "network_outage": "NetworkTimeout",
    "battery_cycle": "PowerFailure",
    "cloud_sync": "SyncError",
    "battery_drains":"BatteryOutage"
}

def generate_simulation_log(
    n_records: int = 1000,
    n_devices: int = 10,
    start_time: datetime = None,
    failure_rate: float = 0.05,
    seed: int = None
) -> pd.DataFrame:
    """
    Generate synthetic simulation log DataFrame.
    Columns: ts, dev, cycle, action, status, error
    """
    if seed is not None:
        np.random.seed(seed)
    if start_time is None:
        start_time = datetime.now()
        
    actions = list(ERROR_TYPES.keys())
    cycle_counters = {d: 0 for d in range(n_devices)}
    rows = []

    for i in range(n_records):
        dev = np.random.randint(0, n_devices)
        action = np.random.choice(actions, p=[0.1, 0.1, 0.1, 0.1, 0.1,0.5])
        if action == "dose_event":
            cycle_counters[dev] += 1
        cycle = cycle_counters[dev]
        ts = start_time + timedelta(seconds=int(np.random.rand() * 3600 * 24))
        status = "FAIL" if np.random.rand() < failure_rate else "PASS"
        error = ERROR_TYPES[action] if status == "FAIL" else ""
        rows.append([ts.isoformat(), dev, cycle, action, status, error])

    df = pd.DataFrame(rows, columns=["ts", "dev", "cycle", "action", "status", "error"])
    df["ts"] = pd.to_datetime(df["ts"])
    return df