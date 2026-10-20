#!/usr/bin/env python3
"""Render two scientific figures from the preserved and recomputed CSVs.

First run: python3 scripts/analyze.py
Then, in an environment with matplotlib:
    python3 scripts/plot_reanalysis.py

Only new figures/reanalysis-* files are written. --data-dir and --output-dir
override the repository defaults. No network access is used by this script.
Figure provenance records source/output hashes and plotting-library versions.
"""

import argparse
import csv
import hashlib
import json
import platform
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy

ROOT = Path(__file__).resolve().parents[1]
HIGH = ("DobeWorks-v2.1", "DEGS-v2.1", "BackspaceTextRetention", "TrashTreasurePickup")


def read(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(figure, output_dir, stem):
    paths = []
    for extension in ("png", "pdf"):
        path = output_dir / f"{stem}.{extension}"
        metadata = {"Creator": "scripts/plot_reanalysis.py", "CreationDate": None,
                    "ModDate": None} if extension == "pdf" else {"Software": "scripts/plot_reanalysis.py"}
        figure.savefig(path, dpi=220, facecolor="white", metadata=metadata)
        paths.append(path)
    plt.close(figure)
    return paths


def window_figure(data_dir, output_dir):
    snapshot = read(data_dir / "traffic-snapshot-2026-10-19.csv")
    windows = read(data_dir / "reanalysis-window-metrics.csv")
    figure, axes = plt.subplots(2, 2, figsize=(10, 7.1), sharex=True, sharey=True)
    figure.subplots_adjust(left=.075, right=.975, top=.85, bottom=.16, hspace=.30, wspace=.10)
    figure.suptitle("Daily clone counts and window sensitivity", fontsize=15, y=.965)
    figure.text(.5, .921, "Preserved follow-up: October 5–18, 2026 (UTC)", ha="center", fontsize=11)
    for letter, name, axis in zip("ABCD", HIGH, axes.flat):
        rows = sorted((row for row in snapshot if row["repository"] == name),
                      key=lambda row: row["date_utc"])
        dates = [datetime.fromisoformat(row["date_utc"]) for row in rows]
        values = [int(row["clones"]) for row in rows]
        axis.axvspan(datetime(2026, 10, 12, 12), datetime(2026, 10, 18, 12),
                     color=".90", linewidth=0)
        axis.axvspan(datetime(2026, 10, 16, 12), datetime(2026, 10, 18, 12),
                     facecolor="none", hatch="////", edgecolor=".65", linewidth=0)
        axis.plot(dates, values, color="black", marker="o", markersize=3.3, linewidth=1)
        axis.set_title(f"{letter}. {name}", loc="left", fontsize=11)
        axis.set_ylim(0, 300)
        axis.set_xlim(datetime(2026, 10, 4, 12), datetime(2026, 10, 18, 12))
        axis.set_yticks([0, 100, 200, 300])
        axis.xaxis.set_major_locator(mdates.DayLocator(bymonthday=[5, 7, 9, 11, 13, 15, 17]))
        axis.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        axis.grid(axis="y", color=".8", linewidth=.5)
        values_by_window = {row["window"]: row for row in windows if row["repository"] == name}
        lines = []
        for label, key in (("14 days", "full_followup_14_days"),
                           ("6 days", "selected_6_days"), ("2 new days", "new_only_2_days")):
            row = values_by_window[key]
            lines.append(f"{label}: range {float(row['range_percent_of_mean']):.2f}%; "
                         f"CV {float(row['sample_cv_percent']):.2f}%")
        axis.text(.035, .055, "\n".join(lines), transform=axis.transAxes, fontsize=8.5,
                  va="bottom", bbox={"facecolor": "white", "edgecolor": "none", "alpha": .9, "pad": 2})
    for axis in axes[:, 0]:
        axis.set_ylabel("GitHub-counted clones")
    figure.legend(handles=[Patch(facecolor=".9", edgecolor="none", label="Selected six days: Oct 13–18"),
                           Patch(facecolor="white", edgecolor=".65", hatch="////",
                                 label="Two dates beyond original window: Oct 17–18")],
                  loc="lower center", bbox_to_anchor=(.5, .075), ncol=2, frameon=False, fontsize=9)
    figure.text(.075, .029,
                "Range = 100 × (max − min) / mean; CV uses sample SD. Shared axes include zero.\n"
                "The selected interval follows observed spikes; the two new dates are not an independent 14-day replication.",
                fontsize=9)
    return save(figure, output_dir, "reanalysis-window-sensitivity")


def comparison_figure(data_dir, output_dir):
    rows = [row for row in read(data_dir / "reanalysis-comparison-series.csv")
            if row["included_in_reanalysis"] == "True"]
    focal = [row for row in read(data_dir / "reanalysis-window-metrics.csv")
             if row["window"] == "selected_6_days" and row["repository"] in HIGH]
    stratum = [row for row in rows if row["in_mean_100_to_200_stratum"] == "True"]
    below_25 = sum(float(row["mean"]) < 25 for row in rows)
    figure, axes = plt.subplots(1, 2, figsize=(10.4, 5.7), sharey=True,
                               gridspec_kw={"width_ratios": [1.2, 1]})
    figure.subplots_adjust(left=.08, right=.975, top=.83, bottom=.23, wspace=.18)
    figure.suptitle("Comparison depends on the underlying clone rate", fontsize=15, y=.965)
    figure.text(.5, .916, "Same six dates: October 13–18, 2026 (UTC)", ha="center", fontsize=11)
    for axis in axes:
        axis.set_yscale("log")
        axis.set_ylim(.8, 900)
        axis.set_yticks([1, 4, 10, 100, 600], ["1", "4", "10", "100", "600"])
        axis.axhline(4, color=".4", linewidth=.8, linestyle="--")
        axis.grid(axis="y", color=".85", linewidth=.5)
        axis.scatter([float(row["mean"]) for row in focal],
                     [float(row["range_percent_of_mean"]) for row in focal],
                     marker="s", facecolor="black", edgecolor="black", s=28,
                     label="Four focal repositories", zorder=4)
        axis.set_xlabel("Mean daily clone count")
    axes[0].scatter([float(row["mean"]) for row in rows],
                    [float(row["range_percent_of_mean"]) for row in rows],
                    marker="o", facecolor="none", edgecolor=".45", linewidth=.7, s=22,
                    label=f"Screened external series (n = {len(rows)})")
    axes[0].set_xscale("log")
    axes[0].set_xlim(.12, 7000)
    axes[0].set_xticks([.2, 1, 10, 100, 1000], [".2", "1", "10", "100", "1,000"])
    axes[0].axvline(25, color=".5", linewidth=.7, linestyle=":")
    axes[0].set_title("A. Broad convenience sample", loc="left", fontsize=11)
    axes[0].set_ylabel("Six-day range / mean (%) — log scale")
    axes[0].text(.04, .40, f"{below_25}/{len(rows)} series average <25/day.\n"
                 "A nonconstant integer series below\n25/day cannot have range/mean ≤4%.",
                 transform=axes[0].transAxes, fontsize=9,
                 bbox={"facecolor": "white", "edgecolor": "none", "alpha": .9})
    axes[1].scatter([float(row["mean"]) for row in stratum],
                    [float(row["range_percent_of_mean"]) for row in stratum],
                    marker="o", facecolor="none", edgecolor=".3", linewidth=1, s=42)
    axes[1].set_xlim(100, 210)
    axes[1].set_xticks([100, 125, 150, 175, 200])
    axes[1].set_title("B. Post hoc 100–200/day stratum", loc="left", fontsize=11)
    axes[1].text(130, 235, "consort\n191.66%", fontsize=9)
    axes[1].text(178, 112, "MegaV_Public\n87.84%", fontsize=9, ha="center")
    axes[1].text(154, 1.45, "Four focal series:\n1.40–3.50%", fontsize=9)
    axes[1].text(103, 4.7, "4% reference", fontsize=8, color=".3")
    handles, labels = axes[0].get_legend_handles_labels()
    figure.legend(handles, labels, loc="lower center", bbox_to_anchor=(.5, .119),
                  ncol=2, frameon=False, fontsize=9)
    figure.text(.08, .045,
                "Cumulative and provenance-ambiguous records are excluded; source-host series can be clustered.\n"
                "Points are plotted without jitter and can overlap. Only two external series meet the rate stratum.\n"
                "This sensitivity analysis is descriptive; it estimates neither population rarity nor causation.", fontsize=9)
    return save(figure, output_dir, "reanalysis-rate-comparison")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "figures")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({
        "font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"],
        "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
        "pdf.fonttype": 42, "ps.fonttype": 42,
    })
    inputs = [args.data_dir / name for name in
              ("traffic-snapshot-2026-10-19.csv", "reanalysis-window-metrics.csv",
               "reanalysis-comparison-series.csv")]
    outputs = window_figure(args.data_dir, args.output_dir) + comparison_figure(args.data_dir, args.output_dir)
    provenance = {
        "script": "scripts/plot_reanalysis.py", "python_version": platform.python_version(),
        "matplotlib_version": matplotlib.__version__, "numpy_version": numpy.__version__,
        "script_sha256": sha(Path(__file__)),
        "inputs": [{"file": "data/" + path.name, "sha256": sha(path)} for path in inputs],
        "outputs": [{"file": "figures/" + path.name, "sha256": sha(path)} for path in outputs],
        "notes": [
            "New scientific plots; original figures are preserved unchanged.",
            "PNG and vector PDF formats contain the same plot content.",
            "The analysis itself uses only Python's standard library; plotting additionally requires matplotlib.",
        ],
    }
    (args.output_dir / "reanalysis-provenance.json").write_text(
        json.dumps(provenance, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(provenance, indent=2))


if __name__ == "__main__":
    main()
