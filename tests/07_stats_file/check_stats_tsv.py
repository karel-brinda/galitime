#!/usr/bin/env python3

import argparse
import csv
import sys


EXPECTED_HEADER = [
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
    "real_s_mean",
    "real_s_stddev",
    "real_s_min",
    "real_s_median",
    "real_s_max",
    "user_s_mean",
    "user_s_stddev",
    "user_s_min",
    "user_s_median",
    "user_s_max",
    "sys_s_mean",
    "sys_s_stddev",
    "sys_s_min",
    "sys_s_median",
    "sys_s_max",
    "cpu_s_mean",
    "cpu_s_stddev",
    "cpu_s_min",
    "cpu_s_median",
    "cpu_s_max",
    "cpu_pct_mean",
    "cpu_pct_stddev",
    "cpu_pct_min",
    "cpu_pct_median",
    "cpu_pct_max",
    "max_ram_kb_mean",
    "max_ram_kb_stddev",
    "max_ram_kb_min",
    "max_ram_kb_median",
    "max_ram_kb_max",
    "command",
]
STDDEV_COLUMNS = [column for column in EXPECTED_HEADER if column.endswith("_stddev")]
NUMERIC_SUMMARY_COLUMNS = [
    column
    for column in EXPECTED_HEADER
    if column.endswith(("_mean", "_stddev", "_min", "_median", "_max"))
]


def die(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--expect-header", action="store_true")
    parser.add_argument("--expect", action="append", default=[])
    parser.add_argument("--all-stddev-na", action="store_true")
    parser.add_argument("--all-numeric-na", action="store_true")
    args = parser.parse_args()

    with open(args.path, newline="") as handle:
        rows = list(csv.reader(handle, delimiter="\t"))

    if len(rows) != len(EXPECTED_HEADER):
        die(
            f"{args.path}: expected exactly {len(EXPECTED_HEADER)} lines, found {len(rows)}"
        )

    for i, row in enumerate(rows, start=1):
        if len(row) != 2:
            die(f"{args.path}: line {i} is not a 2-column TSV row: {row!r}")

    keys = [key for key, _ in rows]
    if args.expect_header and keys != EXPECTED_HEADER:
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
        for key in STDDEV_COLUMNS:
            if row.get(key) != "NA":
                die(f"{args.path}: expected {key}=NA, got {row.get(key)!r}")

    if args.all_numeric_na:
        for key in NUMERIC_SUMMARY_COLUMNS:
            if row.get(key) != "NA":
                die(f"{args.path}: expected {key}=NA, got {row.get(key)!r}")


if __name__ == "__main__":
    main()
