import numpy as np

def detect_peaks(signal):
    """
    Simple peak detection
    """
    peaks = []
    for i in range(1, len(signal) - 1):
        if signal[i] > signal[i - 1] and signal[i] > signal[i + 1]:
            peaks.append(i)
    return peaks