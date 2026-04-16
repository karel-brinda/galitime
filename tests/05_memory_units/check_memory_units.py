#!/usr/bin/env python3

import argparse
import csv
import sys


def load_max_ram_kb(path):
    with open(path, newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(rows) != 1:
        raise RuntimeError(f"{path}: expected exactly 1 data row, found {len(rows)}")
    return int(rows[0]["max_ram_kb"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--small", required=True)
    parser.add_argument("--large", required=True)
    parser.add_argument("--small-mib", type=int, required=True)
    parser.add_argument("--large-mib", type=int, required=True)
    parser.add_argument("--backend", required=True)
    parser.add_argument("--min-bytes-per-unit", type=float, default=850.0)
    parser.add_argument("--max-bytes-per-unit", type=float, default=1150.0)
    args = parser.parse_args()

    small_kb = load_max_ram_kb(args.small)
    large_kb = load_max_ram_kb(args.large)
    reported_delta = large_kb - small_kb
    expected_delta_bytes = (args.large_mib - args.small_mib) * 1024 * 1024

    if reported_delta <= 0:
        print(
            f"{args.backend}: non-positive max_ram_kb delta ({reported_delta}) "
            f"from {small_kb} to {large_kb}",
            file=sys.stderr,
        )
        sys.exit(1)

    bytes_per_reported_unit = expected_delta_bytes / reported_delta
    if not (args.min_bytes_per_unit <= bytes_per_reported_unit <= args.max_bytes_per_unit):
        print(
            f"{args.backend}: expected bytes per reported unit in "
            f"[{args.min_bytes_per_unit}, {args.max_bytes_per_unit}], got "
            f"{bytes_per_reported_unit:.3f} "
            f"(small={small_kb}, large={large_kb}, delta={reported_delta})",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
