#!/usr/bin/env python3

import argparse
import csv
import sys


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tsv")
    parser.add_argument("expected_command")
    parser.add_argument("--rows", type=int, default=1)
    args = parser.parse_args()

    with open(args.tsv, newline="") as fh:
        rows = list(csv.reader(fh, delimiter="\t"))

    if not rows:
        fail(f"{args.tsv} is empty")

    header = rows[0]
    data_rows = rows[1:]

    for column in ("status", "exit_code", "command"):
        if column not in header:
            fail(f"{args.tsv} is missing the {column!r} column")

    if len(data_rows) != args.rows:
        fail(f"{args.tsv} has {len(data_rows)} data rows, expected {args.rows}")

    status_idx = header.index("status")
    exit_code_idx = header.index("exit_code")
    command_idx = header.index("command")

    first_row = data_rows[0]
    if first_row[status_idx] != "ok":
        fail(f"{args.tsv} has status={first_row[status_idx]!r}, expected 'ok'")
    if first_row[exit_code_idx] != "0":
        fail(f"{args.tsv} has exit_code={first_row[exit_code_idx]!r}, expected '0'")
    if first_row[command_idx] != args.expected_command:
        fail(
            f"{args.tsv} has command={first_row[command_idx]!r}, expected {args.expected_command!r}"
        )


if __name__ == "__main__":
    main()
