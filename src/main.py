import argparse

from preprocessing import load_profile, smooth_signal, normalize
from feature_detection import detect_peaks
from geometry_analysis import estimate_basic_metrics


def main(input_path):
    signal = load_profile(input_path)
    smoothed = smooth_signal(signal)
    normalized = normalize(smoothed)
    peaks = detect_peaks(normalized)
    metrics = estimate_basic_metrics(normalized)

    print("Detected Peaks:", peaks)
    print("Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        required=True,
        help="path to 1D sensor profile data"
    )

    args = parser.parse_args()
    main(args.input)