import numpy as np
import pandas as pd

def load_profile(path):
    """Load 1D sensor profile data from CSV"""
    df = pd.read_csv(path)
    return df["value"].values

def smooth_signal(signal, window_size=5):
    """Simple moving average smoothing"""
    kernel = np.ones(window_size) / window_size
    return np.convolve(signal, kernel, mode="same")

def normalize(signal):
    """Normalize signal to 0~1 range"""
    min_v = np.min(signal)
    max_v = np.max(signal)
    return (signal - min_v) / (max_v - min_v)