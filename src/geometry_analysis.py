import numpy as np

def estimate_basic_metrics(signal):
    """
    Estimate basic geometric characteristics
    """
    metrics = {
        "max_value": float(np.max(signal)),
        "min_value": float(np.min(signal)),
        "mean_value": float(np.mean(signal)),
        "std_value": float(np.std(signal)),
    }
    return metrics