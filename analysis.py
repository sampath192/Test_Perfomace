import pandas as pd
import numpy as np
from scipy.stats import weibull_min

def compute_mtbf(df: pd.DataFrame) -> float:
    """
    Compute MTBF (hours) given a simulation log DataFrame.
    """
    start = df.ts.min()
    end = df.ts.max()
    hours_per_device = (end - start).total_seconds() / 3600.0
    total_device_hours = hours_per_device * df.dev.nunique()
    n_fail = df[df.status == "FAIL"].shape[0]
    return total_device_hours / n_fail if n_fail else np.inf

def fit_weibull(df: pd.DataFrame) -> (float):
    """
    Fit a Weibull distribution to time-to-first-failure per device.
    Returns (shape β, scale η).
    """
    failures = df[df.status == "FAIL"].groupby("dev")["ts"].min().reset_index()
    if failures.empty:
        return np.nan, np.nan
    start = df.ts.min()
    ttf = failures.ts.map(lambda t: (t - start).total_seconds() / 3600.0)
    β, loc, η = weibull_min.fit(ttf, floc=0)
    return β, η