#!/usr/bin/env python3

import argparse
import csv
import sys


EXPECTED_HEADER = [
    "experiment",
    "run",
    "real_s",
    "user_s",
    "sys_s",
    "cpu_s",
    "cpu_pct",
    "max_ram_kb",
    "backend",
    "fs_inputs",
    "fs_outputs",
    "major_page_faults",
    "minor_page_faults",
    "swaps",
    "status",
    "exit_code",
    "command",
]


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tsv")
    parser.add_argument("--rows", type=int, default=1)
    parser.add_argument("--expect-header", action="store_true")
    parser.add_argument("--expect", action="append", default=[])
    parser.add_argument("--expect-not-na", action="append", default=[])
    parser.add_argument("--expect-na", action="append", default=[])
    args = parser.parse_args()

    with open(args.tsv, newline="") as fh:
        rows = list(csv.reader(fh, delimiter="\t"))

    if len(rows) != args.rows + 1:
        fail(f"{args.tsv} has {len(rows) - 1} data rows, expected {args.rows}")

    if not rows:
        fail(f"{args.tsv} is empty")

    header = rows[0]
    if args.expect_header and header != EXPECTED_HEADER:
        fail(f"{args.tsv}: unexpected header: {header}")

    if len(set(header)) != len(header):
        fail(f"{args.tsv}: duplicate keys found: {header}")

    if any(len(row) != len(header) for row in rows[1:]):
        bad_row = next(row for row in rows[1:] if len(row) != len(header))
        fail(f"{args.tsv}: malformed data row: {bad_row!r}")

    row = dict(zip(header, rows[1]))

    for item in args.expect:
        if "=" not in item:
            fail(f"invalid expectation: {item!r}")
        key, expected = item.split("=", 1)
        actual = row.get(key)
        if actual != expected:
            fail(f"{args.tsv}: expected {key}={expected!r}, got {actual!r}")

    for key in args.expect_not_na:
        actual = row.get(key)
        if actual in {None, "", "NA"}:
            fail(f"{args.tsv}: expected {key} to be present, got {actual!r}")

    for key in args.expect_na:
        actual = row.get(key)
        if actual != "NA":
            fail(f"{args.tsv}: expected {key}=NA, got {actual!r}")


if __name__ == "__main__":
    main()
