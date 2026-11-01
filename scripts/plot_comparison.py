"""Regenerate the combined accuracy and macro-F1 comparison plots."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "results" / "comparison" / "summary_metrics.csv"
OUTPUT = ROOT / "results" / "comparison"

ORDER = ["Clean", "20 dB", "10 dB", "5 dB", "0 dB"]
COLORS = {
    "MFCC + SVM": "#2878B5",
    "Spectrogram CNN": "#E67E22",
    "YAMNet + SVM": "#2A9D6F",
}
MARKERS = {"MFCC + SVM": "o", "Spectrogram CNN": "s", "YAMNet + SVM": "D"}


def plot_metric(frame: pd.DataFrame, column: str, ylabel: str, filename: str) -> None:
    figure, axis = plt.subplots(figsize=(8.4, 4.8))
    for model, group in frame.groupby("model", sort=False):
        ordered = group.set_index("condition").loc[ORDER]
        axis.plot(
            ORDER,
            100 * ordered[column],
            marker=MARKERS[model],
            linewidth=2.4,
            markersize=7,
            color=COLORS[model],
            label=model,
        )
    if column == "mean_accuracy":
        axis.axhline(2, color="#687986", linestyle="--", linewidth=1, label="Chance baseline")
    axis.set_ylim(0, 90)
    axis.set_xlabel("Evaluation condition")
    axis.set_ylabel(ylabel)
    axis.grid(axis="y", alpha=0.25)
    axis.legend(frameon=False)
    figure.tight_layout()
    figure.savefig(OUTPUT / filename, dpi=220, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    data = pd.read_csv(INPUT)
    plot_metric(data, "mean_accuracy", "Mean five-fold accuracy (%)", "accuracy_vs_snr.png")
    plot_metric(data, "mean_macro_f1", "Mean five-fold macro-F1 (%)", "macro_f1_vs_snr.png")


if __name__ == "__main__":
    main()
