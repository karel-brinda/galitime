#!/usr/bin/env python3

import argparse
import csv
import sys


STATS_PREFIX_COLUMNS = [
    "experiment",
    "runs_requested",
    "runs_completed",
    "runs_summarized",
    "runs_ok",
    "runs_failed",
    "runs_timeout",
    "runs_timing_error",
    "final_status",
    "final_exit_code",
]
STATS_SUFFIX_COLUMNS = ["command"]
STATS_AGGS = ["mean", "stddev", "min", "median", "max"]
BASE_STATS_NUMERIC_METRICS = [
    "real_s",
    "user_s",
    "sys_s",
    "cpu_s",
    "cpu_pct",
    "max_ram_kb",
]
EXTENDED_STATS_NUMERIC_METRICS = BASE_STATS_NUMERIC_METRICS + [
    "fs_inputs",
    "fs_outputs",
    "major_page_faults",
    "minor_page_faults",
    "swaps",
]


def make_stats_columns(metrics):
    columns = list(STATS_PREFIX_COLUMNS)
    for metric in metrics:
        for agg in STATS_AGGS:
            columns.append(f"{metric}_{agg}")
    columns.extend(STATS_SUFFIX_COLUMNS)
    return columns


def die(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--expect-header", action="store_true")
    parser.add_argument("--extended", action="store_true")
    parser.add_argument("--expect", action="append", default=[])
    parser.add_argument("--all-stddev-na", action="store_true")
    parser.add_argument("--all-numeric-na", action="store_true")
    args = parser.parse_args()

    expected_header = make_stats_columns(
        EXTENDED_STATS_NUMERIC_METRICS if args.extended else BASE_STATS_NUMERIC_METRICS
    )
    numeric_summary_columns = [
        column
        for column in expected_header
        if column.endswith(("_mean", "_stddev", "_min", "_median", "_max"))
    ]
    stddev_columns = [column for column in expected_header if column.endswith("_stddev")]

    with open(args.path, newline="") as handle:
        rows = list(csv.reader(handle, delimiter="\t"))

    if len(rows) != len(expected_header):
        die(
            f"{args.path}: expected exactly {len(expected_header)} lines, found {len(rows)}"
        )

    for i, row in enumerate(rows, start=1):
        if len(row) != 2:
            die(f"{args.path}: line {i} is not a 2-column TSV row: {row!r}")

    keys = [key for key, _ in rows]
    if args.expect_header and keys != expected_header:
        die(f"{args.path}: unexpected key order: {keys}")
    if len(set(keys)) != len(keys):
        die(f"{args.path}: duplicate keys found: {keys}")

    row = dict(rows)

    for item in args.expect:
        if "=" not in item:
            die(f"invalid expectation: {item!r}")
        key, expected = item.split("=", 1)
        actual = row.get(key)
        if actual != expected:
            die(f"{args.path}: expected {key}={expected!r}, got {actual!r}")

    if args.all_stddev_na:
        for key in stddev_columns:
            if row.get(key) != "NA":
                die(f"{args.path}: expected {key}=NA, got {row.get(key)!r}")

    if args.all_numeric_na:
        for key in numeric_summary_columns:
            if row.get(key) != "NA":
                die(f"{args.path}: expected {key}=NA, got {row.get(key)!r}")


if __name__ == "__main__":
    main()
